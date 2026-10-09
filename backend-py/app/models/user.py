from datetime import datetime, timedelta

import bcrypt
from psycopg2.errors import UniqueViolation

from ..db import get_db

# Must match the `mood` enum in schema.sql
MOODS = ("good", "okay", "bad")

# Daily calories count as "on target" within this fraction of the goal
CALORIE_TOLERANCE = 0.10

USER_COLUMNS = "id, name, email, password, settings_finished"


def sleep_duration(bedtime, wakeup_time):
    """Hours slept between two "HH:MM" strings, treating an earlier wake time as the next day."""
    start = datetime.strptime(bedtime, "%H:%M")
    end = datetime.strptime(wakeup_time, "%H:%M")
    if end < start:
        end += timedelta(days=1)
    return round((end - start).total_seconds() / 3600, 1)


def goals_met(total_calories, sleep_hours, meals_count, settings):
    """Whether a day's totals satisfy the user's calorie, sleep and meal goals."""
    if not settings:
        return False
    calorie_goal = settings["calories"]
    calories_on_target = abs(total_calories - calorie_goal) <= calorie_goal * CALORIE_TOLERANCE
    return (
        calories_on_target
        and float(sleep_hours) >= settings["sleep"]
        and meals_count >= settings["meals"]
    )


def _format_time(value):
    """"HH:MM" from a time column, which may be TIME (schema.sql) or TEXT (older databases)."""
    if value is None:
        return None
    if isinstance(value, str):
        return value[:5]
    return value.strftime("%H:%M")


class User:
    def __init__(self, id, name, email, password, settings_finished):
        self.id = id
        self.name = name
        self.email = email
        self.password = password  # bcrypt hash, never sent to clients
        self.settings_finished = settings_finished

    @classmethod
    def _find_one(cls, column, value):
        with get_db().cursor() as cur:
            cur.execute(f"SELECT {USER_COLUMNS} FROM users WHERE {column} = %s", (value,))
            row = cur.fetchone()
        return cls(*row) if row else None

    @classmethod
    def find_by_id(cls, user_id):
        return cls._find_one("id", user_id)

    @classmethod
    def find_by_email(cls, email):
        return cls._find_one("email", email)

    @classmethod
    def create(cls, name, email, password):
        """Insert a new user; returns None if the email is already registered."""
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        conn = get_db()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    f"INSERT INTO users (name, email, password, settings_finished) "
                    f"VALUES (%s, %s, %s, FALSE) RETURNING {USER_COLUMNS}",
                    (name, email, hashed)
                )
                row = cur.fetchone()
            conn.commit()
        except UniqueViolation:
            conn.rollback()
            return None
        return cls(*row)

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))

    def to_public_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "settings_finished": self.settings_finished
        }

    def get_settings(self):
        with get_db().cursor() as cur:
            cur.execute("""
                SELECT calories_per_day, bedtime, wakeup_time, sleep_hours, meals_per_day,
                       notifications_sleep, notifications_meals
                FROM user_settings
                WHERE user_id = %s
            """, (self.id,))
            row = cur.fetchone()
        if not row:
            return None
        calories, bedtime, wakeup_time, sleep, meals, notifications_sleep, notifications_meals = row
        return {
            "calories": calories,
            "bedtime": _format_time(bedtime),
            "wakeupTime": _format_time(wakeup_time),
            "sleep": sleep,
            "meals": meals,
            "notificationsSleep": notifications_sleep,
            "notificationsMeals": notifications_meals
        }

    def save_settings(self, calories, meals, sleep, bedtime, wakeup_time,
                      notifications_meals, notifications_sleep):
        conn = get_db()
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO user_settings (user_id, calories_per_day, meals_per_day, sleep_hours,
                                           bedtime, wakeup_time, notifications_sleep,
                                           notifications_meals, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
                ON CONFLICT (user_id) DO UPDATE SET
                    calories_per_day = EXCLUDED.calories_per_day,
                    meals_per_day = EXCLUDED.meals_per_day,
                    sleep_hours = EXCLUDED.sleep_hours,
                    bedtime = EXCLUDED.bedtime,
                    wakeup_time = EXCLUDED.wakeup_time,
                    notifications_sleep = EXCLUDED.notifications_sleep,
                    notifications_meals = EXCLUDED.notifications_meals,
                    updated_at = NOW()
            """, (self.id, calories, meals, sleep, bedtime, wakeup_time,
                  notifications_sleep, notifications_meals))
            cur.execute("UPDATE users SET settings_finished = TRUE WHERE id = %s", (self.id,))
        conn.commit()
        self.settings_finished = True

    def _ensure_daily_log(self, cur):
        cur.execute("""
            INSERT INTO daily_logs (user_id, date)
            VALUES (%s, CURRENT_DATE)
            ON CONFLICT (user_id, date) DO NOTHING
        """, (self.id,))

    def _update_goals(self, cur):
        """Recompute today's goals_met and streak from today's totals and yesterday's streak."""
        cur.execute("""
            SELECT total_calories, sleep_hours, meals_count
            FROM daily_logs
            WHERE user_id = %s AND date = CURRENT_DATE
        """, (self.id,))
        total_calories, sleep_hours, meals_count = cur.fetchone()

        if goals_met(total_calories, sleep_hours, meals_count, self.get_settings()):
            cur.execute("""
                SELECT streak
                FROM daily_logs
                WHERE user_id = %s AND date = CURRENT_DATE - 1 AND goals_met
            """, (self.id,))
            yesterday = cur.fetchone()
            met, streak = True, (yesterday[0] + 1 if yesterday else 1)
        else:
            met, streak = False, 0

        cur.execute("""
            UPDATE daily_logs
            SET goals_met = %s, streak = %s, updated_at = NOW()
            WHERE user_id = %s AND date = CURRENT_DATE
        """, (met, streak, self.id))

    def add_meal(self, calories):
        conn = get_db()
        with conn.cursor() as cur:
            self._ensure_daily_log(cur)
            # Numbering in one statement; a concurrent duplicate fails on the primary key
            cur.execute("""
                INSERT INTO meal_logs (user_id, date, meal_number, calories, created_at)
                SELECT %s, CURRENT_DATE, COALESCE(MAX(meal_number), 0) + 1, %s, NOW()
                FROM meal_logs
                WHERE user_id = %s AND date = CURRENT_DATE
            """, (self.id, calories, self.id))
            cur.execute("""
                UPDATE daily_logs
                SET total_calories = totals.calories, meals_count = totals.meals, updated_at = NOW()
                FROM (
                    SELECT COALESCE(SUM(calories), 0) AS calories, COUNT(*) AS meals
                    FROM meal_logs
                    WHERE user_id = %s AND date = CURRENT_DATE
                ) AS totals
                WHERE user_id = %s AND date = CURRENT_DATE
            """, (self.id, self.id))
            self._update_goals(cur)
        conn.commit()

    def add_sleep(self, bedtime, wakeup_time):
        hours = sleep_duration(bedtime, wakeup_time)
        conn = get_db()
        with conn.cursor() as cur:
            self._ensure_daily_log(cur)
            cur.execute("""
                INSERT INTO sleep_logs (user_id, date, bedtime, wakeup_time, sleep_hours, created_at)
                VALUES (%s, CURRENT_DATE, %s, %s, %s, NOW())
                ON CONFLICT (user_id, date) DO UPDATE SET
                    bedtime = EXCLUDED.bedtime,
                    wakeup_time = EXCLUDED.wakeup_time,
                    sleep_hours = EXCLUDED.sleep_hours,
                    created_at = NOW()
            """, (self.id, bedtime, wakeup_time, hours))
            cur.execute("""
                UPDATE daily_logs
                SET sleep_hours = %s, updated_at = NOW()
                WHERE user_id = %s AND date = CURRENT_DATE
            """, (hours, self.id))
            self._update_goals(cur)
        conn.commit()
        return hours

    def set_mood(self, mood):
        conn = get_db()
        with conn.cursor() as cur:
            self._ensure_daily_log(cur)
            cur.execute("""
                UPDATE daily_logs
                SET mood = %s, updated_at = NOW()
                WHERE user_id = %s AND date = CURRENT_DATE
            """, (mood, self.id))
        conn.commit()

    def get_daily_log(self):
        with get_db().cursor() as cur:
            cur.execute("""
                SELECT total_calories, sleep_hours, meals_count, goals_met, streak, mood
                FROM daily_logs
                WHERE user_id = %s AND date = CURRENT_DATE
            """, (self.id,))
            row = cur.fetchone()
        if not row:
            return None
        total_calories, sleep_hours, meals_count, met, streak, mood = row
        return {
            "total_calories": total_calories,
            "sleep_hours": float(sleep_hours),
            "meals_count": meals_count,
            "goals_met": met,
            "streak": streak,
            "mood": mood
        }

    def get_recent_logs(self, days=5):
        """Logs for the last `days` days including today, newest first."""
        with get_db().cursor() as cur:
            cur.execute("""
                SELECT date, mood, sleep_hours, total_calories
                FROM daily_logs
                WHERE user_id = %s AND date > CURRENT_DATE - %s
                ORDER BY date DESC
            """, (self.id, days))
            rows = cur.fetchall()
        return [
            {
                "date": log_date.isoformat(),
                "mood": mood,
                "sleep_hours": float(sleep_hours),
                "calories": calories
            }
            for log_date, mood, sleep_hours, calories in rows
        ]
