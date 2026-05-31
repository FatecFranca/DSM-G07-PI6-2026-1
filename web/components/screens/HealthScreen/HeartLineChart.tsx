"use client";

import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { HeartbeatData } from "@/services/animalStatsService";

const CustomizedTick = ({ x, y, payload, compact }: any) => {
  const tickItem = payload.value;
  let datePart = "";
  let timePart = "";

  try {
    if (tickItem && typeof tickItem === "string" && tickItem.includes("-") && tickItem.length >= 10) {
      const baseDate = tickItem.split("T")[0].split(" ")[0]; // "2025-10-17"
      const parts = baseDate.split("-");
      datePart = parts.length >= 3 ? `${parts[2]}/${parts[1]}` : tickItem;

      if (tickItem.includes(" ") || tickItem.includes("T")) {
        timePart = tickItem.includes(" ")
          ? tickItem.split(" ")[1].substring(0, 5)
          : tickItem.split("T")[1].substring(0, 5); // "20:00"
      }
    } else {
      datePart = tickItem;
    }
  } catch {
    datePart = tickItem;
  }

  if (compact && timePart) {
    return (
      <g transform={`translate(${x},${y})`}>
        <text x={0} y={0} textAnchor="middle" fill="var(--color-brown)" fontSize={9} fontWeight={500}>
          <tspan x={0} dy={10}>{datePart}</tspan>
          <tspan x={0} dy={11}>{timePart}</tspan>
        </text>
      </g>
    );
  }

  const fullText = timePart ? `${datePart} ${timePart}` : datePart;
  return (
    <g transform={`translate(${x},${y})`}>
      <text x={0} y={0} dy={10} textAnchor="middle" fill="var(--color-brown)" fontSize={10} fontWeight={500}>
        {fullText}
      </text>
    </g>
  );
};

interface Props {
  title: string;
  data: HeartbeatData[];
  backgroundColor?: string;
  chartHeight?: number;
  compact?: boolean;
}

export default function HeartLineChart({
  title,
  data,
  backgroundColor = "var(--color-sand-900)",
  chartHeight = 220,
  compact = false,
}: Props) {
  if (data.length === 0) {
    return (
      <div
        style={{ backgroundColor }}
        className="w-full rounded-[24px] p-6 shadow-md flex items-center justify-center min-h-[200px]"
      >
        <span className="text-[var(--color-brown)] font-medium">Sem dados para exibir.</span>
      </div>
    );
  }

  // Calculate minY and maxY matching the Flutter logic
  const values = data.map((d) => d.bpm);
  const minValue = Math.min(...values);
  const maxValue = Math.max(...values);

  const minY = Math.max(0, Math.floor(minValue / 10) * 10 - 10);
  const maxY = Math.ceil((maxValue + 1) / 10) * 10 + 10;

  return (
    <div
      style={{ backgroundColor }}
      className={`w-full rounded-[24px] shadow-md flex flex-col items-center ${
        compact ? "p-3 pb-4" : "p-6"
      }`}
    >
      <h3 className={`text-[var(--color-orange-900)] font-bold text-[14px] text-center ${
        compact ? "mb-2" : "mb-6"
      }`}>
        {title}
      </h3>

      <div className="w-full" style={{ height: chartHeight }}>
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart
            data={data}
            margin={{
              top: 5,
              right: compact ? 20 : 10,
              left: -20,
              bottom: compact ? 22 : 5,
            }}
          >
            <defs>
              <linearGradient id="colorBpm" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="var(--color-primary)" stopOpacity={0.2} />
                <stop offset="95%" stopColor="var(--color-primary)" stopOpacity={0.0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="rgba(117, 72, 25, 0.15)" />
            <XAxis
              dataKey="data"
              axisLine={false}
              tickLine={false}
              tick={(props: any) => <CustomizedTick {...props} compact={compact} />}
              interval={0}
            />
            <YAxis
              domain={[minY, maxY]}
              axisLine={false}
              tickLine={false}
              tick={{ fill: "var(--color-brown)", fontSize: 11 }}
            />
            <Tooltip
              cursor={{ stroke: "var(--color-primary)", strokeWidth: 1, strokeDasharray: "3 3" }}
              contentStyle={{
                borderRadius: "12px",
                border: "none",
                boxShadow: "0 4px 10px rgba(0, 0, 0, 0.1)",
                color: "var(--color-brown)",
                backgroundColor: "#fff",
                fontSize: "12px",
              }}
              itemStyle={{ color: "var(--color-primary)", fontWeight: "bold" }}
            />
            <Area
              type="monotone"
              dataKey="bpm"
              stroke="var(--color-primary)"
              strokeWidth={3}
              fillOpacity={1}
              fill="url(#colorBpm)"
              activeDot={{ r: 6, fill: "var(--color-primary)", strokeWidth: 2, stroke: "#fff" }}
              dot={{ r: 3.5, fill: "var(--color-primary)", strokeWidth: 1.5, stroke: "#fff" }}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
