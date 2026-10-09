import {
    ResponsiveContainer,
    ComposedChart,
    Line,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
  } from "recharts";
  
  export default function SleepVsCalories({ data }) {
    return (
      <div className="bg-white p-4 rounded-2xl shadow-md w-full max-w-3xl mx-auto">
        <h2 className="text-sm font-bold uppercase tracking-widest mb-3">
          SLEEP VS CALORIES
        </h2>
        <ResponsiveContainer width="100%" height={300}>
          <ComposedChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis
              yAxisId="left"
              label={{ value: "Sleep (h)", angle: -90, position: "insideLeft" }}
            />
            <YAxis
              yAxisId="right"
              orientation="right"
              label={{ value: "Calories", angle: 90, position: "insideRight" }}
            />
            <Tooltip />
            <Legend />
            <Bar
              yAxisId="right"
              dataKey="calories"
              fill="#10b981"
              name="Calories"
              barSize={20}
            />
            <Line
              yAxisId="left"
              type="monotone"
              dataKey="sleep_hours"
              stroke="#0ea5e9"
              name="Sleep (h)"
              dot
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    );
  }
  