import { useNavigate } from "react-router-dom";
import { Circle } from 'rc-progress';

function getTimeUntil(targetTimeStr) {
  const now = new Date();
  const target = new Date();

  const [hours, minutes] = targetTimeStr.split(':');
  target.setHours(parseInt(hours));
  target.setMinutes(parseInt(minutes));
  target.setSeconds(0);

  if (target <= now) {
    target.setDate(target.getDate() + 1);
  }

  const diffMs = target - now;
  const diffMin = Math.floor(diffMs / 1000 / 60);
  const hoursLeft = Math.floor(diffMin / 60);
  const minutesLeft = diffMin % 60;

  const totalDayMinutes = 24 * 60;
  const percentage = ((totalDayMinutes - diffMin) / totalDayMinutes) * 100;

  return {
    timeRemaining: `${hoursLeft}h ${minutesLeft}m`,
    percentage,
  };
}

function isAsleep(bedtimeStr, wakeupStr) {
  const now = new Date();
  const bedtime = new Date();
  const wakeup = new Date();

  const [bedH, bedM] = bedtimeStr.split(':');
  const [wakeH, wakeM] = wakeupStr.split(':');

  bedtime.setHours(parseInt(bedH));
  bedtime.setMinutes(parseInt(bedM));
  bedtime.setSeconds(0);

  wakeup.setHours(parseInt(wakeH));
  wakeup.setMinutes(parseInt(wakeM));
  wakeup.setSeconds(0);

  if (wakeup <= bedtime) {
    wakeup.setDate(wakeup.getDate() + 1);
  }

  return now >= bedtime && now < wakeup;
}

const SleepCard = ({ bedtime = '22:00', wakeupTime = '06:30' }) => {
  const navigate = useNavigate();

  const asleep = isAsleep(bedtime, wakeupTime);
  const target = asleep ? wakeupTime : bedtime;
  const label = asleep ? 'until wake' : 'until bed';

  const { timeRemaining, percentage } = getTimeUntil(target);

  const handleAddSleepClick = () => {
    navigate("/add-sleep");
  };

  return (
    <div className="bg-blue-200 p-4 rounded-2xl shadow-md w-full max-w-xs text-center text-blue-900 relative">
      <h2 className="text-sm font-bold tracking-widest mb-2">SLEEP</h2>

      <div className="relative w-24 h-24 mx-auto mb-2">
        <Circle
          percent={percentage}
          strokeWidth={8}
          strokeColor="#0ea5e9"
          trailColor="#bae6fd"
        />
        <div className="absolute inset-0 flex flex-col items-center justify-center text-sm font-semibold">
          <div>{timeRemaining}</div>
          <div className="text-xs text-blue-800">{label}</div>
        </div>
      </div>

      <div className="text-sm space-y-1">
        <p><span className="font-medium">Bed Time:</span> {bedtime}</p>
        <p><span className="font-medium">Wake Time:</span> {wakeupTime}</p>
      </div>

      {/* Add Sleep Button */}
      <button
        type="button"
        aria-label="Add sleep"
        className="absolute bottom-4 right-4 bg-white p-2 rounded-full shadow-md cursor-pointer"
        onClick={handleAddSleepClick}
      >
        <span className="text-lg text-blue-500 font-semibold">+</span>
      </button>
    </div>
  );
};

export default SleepCard;




