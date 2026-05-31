"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { HeartbeatData } from "@/services/animalStatsService";

interface Props {
  title: string;
  data: HeartbeatData[];
}

export default function HeartChartBar({ title, data }: Props) {
  const formatXAxis = (tickItem: string) => {
    try {
      if (!tickItem || typeof tickItem !== "string") return tickItem;
      if (tickItem.includes("-") && tickItem.length >= 10) {
        const baseDate = tickItem.split("T")[0].split(" ")[0]; // "2025-10-17"
        const parts = baseDate.split("-");
        const formattedDate = parts.length >= 3 ? `${parts[2]}/${parts[1]}` : tickItem;

        // Check if there is time component
        if (tickItem.includes(" ") || tickItem.includes("T")) {
          const timePart = tickItem.includes(" ")
            ? tickItem.split(" ")[1].substring(0, 5)
            : tickItem.split("T")[1].substring(0, 5); // "20:00"
          return `${formattedDate} ${timePart}`;
        }
        return formattedDate;
      }
      return tickItem;
    } catch {
      return tickItem;
    }
  };

  return (
    <div className="w-full bg-[var(--color-sand-900)] rounded-[24px] p-6 shadow-md flex flex-col items-center">
      <h3 className="text-[var(--color-orange-900)] font-bold text-[14px] text-center mb-6">
        {title}
      </h3>

      <div className="w-full h-[200px]">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            margin={{
              top: 5,
              right: 5,
              left: -20,
              bottom: 5,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="rgba(117, 72, 25, 0.15)" />
            <XAxis
              dataKey="data"
              axisLine={false}
              tickLine={false}
              tick={{ fill: "var(--color-brown)", fontSize: 12 }}
              tickFormatter={formatXAxis}
              dy={10}
            />
            <YAxis
              axisLine={false}
              tickLine={false}
              tick={{ fill: "var(--color-brown)", fontSize: 12 }}
            />
            <Tooltip
              cursor={{ fill: "rgba(243, 146, 0, 0.08)" }}
              contentStyle={{
                borderRadius: "12px",
                border: "none",
                boxShadow: "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                color: "var(--color-brown)",
                backgroundColor: "#fff",
              }}
              itemStyle={{ color: "var(--color-primary)", fontWeight: "bold" }}
            />
            <Bar
              dataKey="bpm"
              fill="var(--color-primary)" // Laranja do app (centralizar mapa)
              radius={[4, 4, 0, 0]}
              barSize={32}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
