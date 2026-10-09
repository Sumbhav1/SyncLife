import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

const CalorieGraph = ({ data }) => {
  const graphData = data
    .map((log) => ({
      date: log.date,
      calories: log.calories,
    }))
    .reverse();

  return (
    <div className="bg-white rounded-xl p-6 shadow-inner w-full max-w-xs">
      <h2 className="text-lg  font-bold mb-4 text-center">
        Calorie Intake (Past 5 Days)
      </h2>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={graphData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="calories" fill="#60a5fa" name="Calories" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default CalorieGraph;
