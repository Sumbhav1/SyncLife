import { Moon, Utensils } from "lucide-react";
import { Card } from "./Card";

export default function CombinedStreakBadge({ days = 7 }) {
  return (
    <Card className="w-[240px] h-[190px] bg-red-400 shadow-md rounded-xl flex flex-col items-center justify-center">
      <p className="mt-4 text-center font-semibold text-gray-700 uppercase tracking-wide">
        Healthy Streak
      </p>
      <div className="relative w-24 h-24 rounded-full bg-yellow-300 shadow-lg flex flex-col items-center justify-center">
        <div className="flex space-x-1 items-center">
          <Utensils className="text-yellow-800 w-5 h-5" />
          <Moon className="text-yellow-800 w-5 h-5" />
        </div>
        <span className="text-sm text-yellow-900 font-semibold mt-1">
          {days}-DAY
        </span>
      </div>
    </Card>
  );
}
