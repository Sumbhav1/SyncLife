import React, { useState } from "react";
import SyncLife from "../assets/images/SyncLife.png";
import { useNavigate } from "react-router-dom";
import api from "../api";

const AddAMeal = () => {
  const [ingredientInput, setIngredientInput] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [mealIngredients, setMealIngredients] = useState([]);
  const [totalCalories, setTotalCalories] = useState(0);
  const [weight, setWeight] = useState(100);
  const [error, setError] = useState("");
  const [successMessage, setSuccessMessage] = useState(""); // State for success message
  const navigate = useNavigate();

  // Ingredient lookups go through our backend, which holds the Spoonacular key
  const searchIngredient = async () => {
    setError("");
    try {
      const response = await api.get("/ingredients/search", {
        params: { query: ingredientInput },
      });
      setSearchResults(response.data.results);
    } catch (err) {
      console.error(err);
      setError("Failed to search ingredients.");
    }
  };

  const addIngredientToMeal = async (ingredient) => {
    setError("");
    try {
      const response = await api.get(`/ingredients/${ingredient.id}/calories`, {
        params: { grams: weight || 100 },
      });

      const ingredientWithCalories = {
        name: ingredient.name,
        calories: response.data.calories,
      };

      setMealIngredients((prev) => [...prev, ingredientWithCalories]);
      setTotalCalories((prev) => prev + ingredientWithCalories.calories);
      setSearchResults([]);
      setIngredientInput("");
      setWeight(100);
    } catch (err) {
      console.error(err);
      setError("Failed to fetch ingredient information.");
    }
  };

  const handleMeal = async () => {
    if (mealIngredients.length === 0) {
      setError("Add at least one ingredient first.");
      return;
    }
    setError("");
    try {
      await api.post("/meals/add", { total_calories: totalCalories });
      // Clear the meal so pressing "Add Meal" again doesn't log it twice
      setMealIngredients([]);
      setTotalCalories(0);
      setSuccessMessage("Meal added successfully!");
      setTimeout(() => setSuccessMessage(""), 3000); // Clear the message after 3 seconds
    } catch (err) {
      console.error("Could not add meal:", err);
      setError("Failed to add meal.");
    }
  };

  const removeIngredientFromMeal = (ingredientIndex) => {
    const updatedMealIngredients = [...mealIngredients];
    const removedIngredient = updatedMealIngredients.splice(
      ingredientIndex,
      1
    )[0];

    setMealIngredients(updatedMealIngredients);
    setTotalCalories((prev) => prev - removedIngredient.calories);
  };

  // Back button navigation handler
  const goBack = () => {
    navigate("/dashboard"); // Replace "/dashboard" with the actual route of the dashboard page
  };

  return (
    <div className="relative flex items-center justify-center min-h-screen bg-blue-300">
      <button
        onClick={goBack}
        className="absolute top-4 left-4 text-white text-2xl bg-transparent hover:bg-gray-600 p-2 rounded-full"
      >
        &#8592; 
      </button>

      <div className="bg-blue-200 p-10 rounded-lg shadow-lg w-96 text-center">
        <div className="flex justify-center mb-5">
          <img
            src={SyncLife}
            alt="SyncLife Logo"
            className="w-24 h-24 rounded-lg"
          />
        </div>
        <p className="mt-2 text-lg font-medium">Add a Meal</p>

        {error && <p className="text-red-500">{error}</p>}
        {successMessage && <p className="text-green-500">{successMessage}</p>} {/* Success message */}

        <div className="mt-4 space-y-4">
          <input
            type="text"
            value={ingredientInput}
            onChange={(e) => setIngredientInput(e.target.value)}
            placeholder="Search for an ingredient..."
            className="w-full px-4 py-2 rounded-lg border border-gray-400 focus:ring focus:ring-blue-500"
          />
          <input
            type="number"
            value={weight}
            onChange={(e) => setWeight(e.target.value)}
            placeholder="Enter weight (g)"
            className="w-full px-4 py-2 rounded-lg border border-gray-400 focus:ring focus:ring-blue-500"
          />
          <button
            onClick={searchIngredient}
            className="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 transition"
          >
            Search Ingredient
          </button>
        </div>

        {searchResults.length > 0 && (
          <div className="mt-4">
            <p className="font-medium">Results:</p>
            <ul className="mt-2 space-y-2">
              {searchResults.map((ingredient) => (
                <li key={ingredient.id}>
                  <button
                    onClick={() => addIngredientToMeal(ingredient)}
                    className="bg-white border border-gray-300 px-3 py-1 rounded-lg hover:bg-blue-100 transition w-full"
                  >
                    {ingredient.name}
                  </button>
                </li>
              ))}
            </ul>
          </div>
        )}

        <div className="mt-6">
          <h3 className="font-semibold">Meal Ingredients:</h3>
          <ul className="mt-2 space-y-1">
            {mealIngredients.map((item, index) => (
              <li
                key={index}
                className="flex justify-between items-center text-sm"
              >
                <span>
                  {item.name} - {item.calories.toFixed(0)} kcal
                </span>
                <button
                  onClick={() => removeIngredientFromMeal(index)}
                  className="text-red-500 hover:text-red-700"
                >
                  X
                </button>
              </li>
            ))}
          </ul>

          <div className="mt-4 font-bold">
            Total Calories: {totalCalories.toFixed(0)} kcal
          </div>
          <button
            onClick={handleMeal}
            className="w-full mt-4 bg-green-500 text-white py-2 rounded-lg hover:bg-green-600 transition"
          >
            Add Meal
          </button>
        </div>
      </div>
    </div>
  );
};

export default AddAMeal;

