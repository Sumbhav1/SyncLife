from datetime import time
from decimal import Decimal

import pytest

from app.models.user import _format_time, goals_met, sleep_duration

SETTINGS = {"calories": 2000, "sleep": 8, "meals": 3}


@pytest.mark.parametrize("bedtime, wakeup, hours", [
    ("22:00", "06:00", 8.0),
    ("23:30", "07:15", 7.8),
    ("01:00", "09:00", 8.0),
    ("07:00", "07:00", 0.0),
])
def test_sleep_duration(bedtime, wakeup, hours):
    assert sleep_duration(bedtime, wakeup) == hours


def test_goals_met_allows_calories_near_target():
    # Previously required calories to equal the goal exactly
    assert goals_met(1950, Decimal("8.0"), 3, SETTINGS)
    assert goals_met(2190, Decimal("8.5"), 4, SETTINGS)


def test_goals_not_met_when_any_goal_missed():
    assert not goals_met(1500, Decimal("8.0"), 3, SETTINGS)   # too few calories
    assert not goals_met(2500, Decimal("8.0"), 3, SETTINGS)   # too many calories
    assert not goals_met(2000, Decimal("6.0"), 3, SETTINGS)   # too little sleep
    assert not goals_met(2000, Decimal("8.0"), 2, SETTINGS)   # too few meals


def test_goals_not_met_without_settings():
    assert not goals_met(2000, Decimal("8.0"), 3, None)


@pytest.mark.parametrize("value, expected", [
    (time(22, 5), "22:05"),
    ("22:05", "22:05"),       # TEXT column in older databases
    ("07:03:00", "07:03"),
    (None, None),
])
def test_format_time_accepts_time_and_text_columns(value, expected):
    assert _format_time(value) == expected
