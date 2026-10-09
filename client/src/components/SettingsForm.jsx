import { useEffect, useState } from "react";
import api from "../api";
import { useAuth } from "./AuthContext";

const inputClass =
  "w-full px-4 py-2 rounded-lg border border-gray-400 focus:ring focus:ring-blue-500";

const YesNo = ({ name, label, value, onChange }) => (
  <div className="text-left">
    <label className="block font-medium">{label}</label>
    <div className="flex space-x-4">
      {[true, false].map((option) => (
        <label key={String(option)} className="inline-flex items-center">
          <input
            type="radio"
            name={name}
            checked={value === option}
            onChange={() => onChange(option)}
            className="mr-2"
          />
          {option ? "Yes" : "No"}
        </label>
      ))}
    </div>
  </div>
);

/**
 * Shared by first-time setup and the logged-in settings page.
 * Calls onSaved(user) after a successful save; shows a back button if onBack is given.
 */
const SettingsForm = ({ onSaved, onBack }) => {
  const { updateUser } = useAuth();
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  const [calories, setCalories] = useState("");
  const [sleep, setSleep] = useState("");
  const [bedtime, setBedtime] = useState("");
  const [wakeupTime, setWakeupTime] = useState("");
  const [meals, setMeals] = useState("");
  const [notificationsSleep, setNotificationsSleep] = useState(false);
  const [notificationsMeals, setNotificationsMeals] = useState(false);

  useEffect(() => {
    api
      .get("/settings/fetch")
      .then(({ data }) => {
        setCalories(data.calories);
        setSleep(data.sleep);
        setBedtime(data.bedtime);
        setWakeupTime(data.wakeupTime);
        setMeals(data.meals);
        setNotificationsSleep(Boolean(data.notificationsSleep));
        setNotificationsMeals(Boolean(data.notificationsMeals));
      })
      .catch((err) => {
        // 404 just means this user hasn't saved settings yet
        if (err.response?.status !== 404) {
          setError("Could not load your current settings.");
        }
      });
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (!calories || !sleep || !bedtime || !wakeupTime || !meals) {
      setError("All fields must be filled out");
      return;
    }

    setLoading(true);
    try {
      const response = await api.post("/settings/set", {
        calories,
        bedtime,
        wakeupTime,
        sleep,
        meals,
        notificationsSleep,
        notificationsMeals,
      });
      updateUser(response.data.user);
      setSuccess("Settings saved successfully!");
      onSaved?.(response.data.user);
    } catch (err) {
      setError(err.response?.data?.error ?? "Unable to save settings. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center h-screen bg-blue-300">
      {onBack && (
        <button
          onClick={onBack}
          aria-label="Back to dashboard"
          className="absolute top-4 left-4 text-white text-2xl bg-transparent hover:bg-gray-600 p-2 rounded-full"
        >
          &#8592;
        </button>
      )}
      <div className="bg-blue-200 p-10 rounded-lg shadow-lg w-96 text-center max-h-screen overflow-auto">
        <h1 className="text-2xl font-semibold mb-6">Settings</h1>

        {error && <p className="text-red-600 mb-4">{error}</p>}
        {success && <p className="text-green-700 mb-4">{success}</p>}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="text-left">
            <label className="block font-medium">Calories per day:</label>
            <input
              type="number"
              min="1"
              value={calories}
              onChange={(e) => setCalories(e.target.value)}
              className={inputClass}
            />
          </div>

          <div className="text-left">
            <label className="block font-medium">Bedtime (hh:mm):</label>
            <input
              type="time"
              value={bedtime}
              onChange={(e) => setBedtime(e.target.value)}
              className={inputClass}
            />
          </div>

          <div className="text-left">
            <label className="block font-medium">Wake-up time (hh:mm):</label>
            <input
              type="time"
              value={wakeupTime}
              onChange={(e) => setWakeupTime(e.target.value)}
              className={inputClass}
            />
          </div>

          <div className="text-left">
            <label className="block font-medium">Hours of sleep:</label>
            <input
              type="number"
              min="0"
              max="24"
              step="0.5"
              value={sleep}
              onChange={(e) => setSleep(e.target.value)}
              className={inputClass}
            />
          </div>

          <div className="text-left">
            <label className="block font-medium">
              How many meals do you (typically) eat per day?
            </label>
            <input
              type="number"
              min="1"
              value={meals}
              onChange={(e) => setMeals(e.target.value)}
              className={inputClass}
            />
          </div>

          <YesNo
            name="notificationsSleep"
            label="Receive reminders to log sleep?"
            value={notificationsSleep}
            onChange={setNotificationsSleep}
          />
          <YesNo
            name="notificationsMeals"
            label="Receive reminders to log meals?"
            value={notificationsMeals}
            onChange={setNotificationsMeals}
          />

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 transition disabled:opacity-60"
          >
            {loading ? "Saving..." : "Save Settings"}
          </button>
        </form>

        <p className="mt-4 text-sm">
          Unsure about how many calories you need?{" "}
          <a
            href="https://www.calculator.net/calorie-calculator.html"
            target="_blank"
            className="text-blue-600 font-semibold underline"
            rel="noopener noreferrer"
          >
            Here's a calorie calculator
          </a>{" "}
          (Please be aware these are just estimates and not official advice)
        </p>
      </div>
    </div>
  );
};

export default SettingsForm;
