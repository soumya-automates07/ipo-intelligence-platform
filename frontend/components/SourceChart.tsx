"use client";

import { PieChart, Pie } from "recharts";

export default function SourceChart() {
  return (
    <PieChart width={300} height={250}>
      <Pie
        data={[
          { value: 10 },
          { value: 20 }
        ]}
        dataKey="value"
      />
    </PieChart>
  );
}