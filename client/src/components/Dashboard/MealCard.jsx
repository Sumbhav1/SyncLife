import { useNavigate } from "react-router-dom";
import { Circle } from 'rc-progress';

const MealCard = ({
  mealsConsumed = 0,
  mealsNeeded = 3,
  caloriesConsumed = 0,
  caloriesNeeded = 2000,
}) => {
  const navigate = useNavigate();

  const percentOf = (value, goal) => (goal > 0 ? (value / goal) * 100 : 0);
  const caloriePercentage = percentOf(caloriesConsumed, caloriesNeeded);
  const mealPercentage = percentOf(mealsConsumed, mealsNeeded);

  const handleAddMealClick = () => {
    navigate("/add-a-meal"); 
  };

  return (
    <div className="bg-green-200 p-4 rounded-2xl shadow-md w-full max-w-xs text-center text-green-900 relative">
      <h2 className="text-sm font-bold tracking-widest mb-2">MEALS</h2>

      <div className="mb-4">
        <div className="text-sm">
          <span className="font-medium">{caloriesConsumed}</span>/
          <span className="font-medium">{caloriesNeeded}</span> calories
        </div>
        <div className="relative w-28 h-28 mx-auto mb-2">
          <Circle
            percent={Math.min(caloriePercentage, 100)}
            strokeWidth={12}  
            strokeColor="#10b981" 
            trailColor="#d1fae5"
            className="rounded-full"
          />
          <div className="absolute inset-0 flex items-center justify-center text-sm font-semibold">
            <span>{caloriePercentage.toFixed(0)}%</span>
          </div>
        </div>
      </div>

      <div className="mb-4">
        <div className="text-sm">
          <span className="font-medium">{mealsConsumed}</span>/
          <span className="font-medium">{mealsNeeded}</span> meals
        </div>
        <div className="relative w-28 h-28 mx-auto mb-2">
          <Circle
            percent={Math.min(mealPercentage, 100)}
            strokeWidth={12}  
            strokeColor="#34d399"  
            trailColor="#d1fae5"
            className="rounded-full"
          />
          <div className="absolute inset-0 flex items-center justify-center text-sm font-semibold">
            <span>{mealPercentage.toFixed(0)}%</span>
          </div>
        </div>
      </div>

      {/* Add Meal Button */}
      <button
        type="button"
        aria-label="Add a meal"
        className="absolute bottom-4 right-4 bg-white p-2 rounded-full shadow-md cursor-pointer"
        onClick={handleAddMealClick}
      >
        <span className="text-lg text-green-500 font-semibold">+</span>
      </button>
    </div>
  );
};

export default MealCard;

