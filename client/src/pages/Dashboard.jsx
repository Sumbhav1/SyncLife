import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import { useAuth } from "../components/AuthContext";

import SyncLife from "../assets/images/SyncLife.png";
import SleepCard from "../components/Dashboard/SleepCard";
import MealCard from "../components/Dashboard/MealCard";
import CombinedStreakBadge from "../components/Dashboard/Streak";
import MoodSelector from "../components/Dashboard/MoodSelector";
import SleepVsCalories from "../components/Dashboard/Correlation";

function getGreeting(name) {
  const hour = new Date().getHours();
  let greeting = "";
  if (hour < 12) greeting = "Good morning";
  else if (hour < 18) greeting = "Good afternoon";
  else greeting = "Good evening";
  return `${greeting}, ${name}`;
}

const Dashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const [data, setData] = useState(null);
  const [mood, setMood] = useState(null);

  useEffect(() => {
    api
      .get("/dashboard/fetch")
      .then((response) => {
        setData(response.data.payload);
        setMood(response.data.payload.dailyLog.mood);
      })
      .catch((err) => {
        console.error(err);
        setError("Couldn't fetch data: " + err.message);
      });
  }, []);

  return (
    <>
      {/* Header */}
      <div className="flex items-center justify-between bg-blue-500 text-white p-4 shadow rounded-b-lg">
        <div className="flex items-center">
          <img src={SyncLife} alt="SyncLife logo" className="h-10 w-10 mr-4" />
          <div>
            <h1 className="text-lg font-semibold">{getGreeting(user.name)}</h1>
            <p className="text-sm opacity-90">
              Here's your progress for the day.
            </p>
          </div>
        </div>
        <button
          onClick={() => navigate("/settings-logged-in")}
          className="bg-white text-blue-500 font-semibold px-4 py-2 rounded-lg shadow hover:bg-gray-100 transition"
        >
          Settings
        </button>
      </div>

      {/* Error message */}
      {error && <p className="text-red-500 text-center font-medium mt-4">{error}</p>}

      {!data && !error && <p className="text-center mt-8">Loading...</p>}

      {data && (
        <>
          {/* First row of cards */}
          <div className="flex flex-wrap justify-start items-start p-4 gap-4">
            <div className="flex-1 min-w-[240px]">
              <SleepCard
                bedtime={data.settings.bedtime}
                wakeupTime={data.settings.wakeupTime}
              />
            </div>
            <div className="flex-1 min-w-[240px]">
              <MealCard
                mealsConsumed={data.dailyLog.meals_count}
                mealsNeeded={data.settings.mealsNeeded}
                caloriesConsumed={data.dailyLog.total_calories}
                caloriesNeeded={data.settings.caloriesNeeded}
              />
            </div>
            <div className="flex-none">
              <CombinedStreakBadge days={data.dailyLog.streak} />
            </div>
            <div className="flex-1 min-w-[240px]">
              <MoodSelector mood={mood} onMoodChange={setMood} />
            </div>
          </div>

          {/* Graph below the first row */}
          {data.recentLogs.length > 0 && (
            <div className="px-4 pt-6 pl-6">
              <SleepVsCalories data={[...data.recentLogs].reverse()} />
            </div>
          )}
        </>
      )}
    </>
  );
};

export default Dashboard;
