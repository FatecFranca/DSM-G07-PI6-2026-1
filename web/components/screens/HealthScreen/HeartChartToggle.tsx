"use client";

import { useState } from "react";
import {
  AreaChart,
  Area,
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
  horasData: HeartbeatData[];
  diasData: HeartbeatData[];
}

// Componente customizado para Tooltip, seguro contra avisos de NaN no React 19 e estilizado com visual premium
const CustomTooltip = ({ active, payload }: any) => {
  if (active && payload && payload.length) {
    const value = payload[0].value;
    const label = payload[0].payload.data;
    
    let formattedLabel = label;
    if (label && typeof label === "string" && label.includes("-") && label.length >= 10) {
      try {
        const baseDate = label.split("T")[0].split(" ")[0]; // "2025-10-17"
        const parts = baseDate.split("-");
        const formattedDate = parts.length >= 3 ? `${parts[2]}/${parts[1]}` : label;

        if (label.includes(" ") || label.includes("T")) {
          const timePart = label.includes(" ")
            ? label.split(" ")[1].substring(0, 5)
            : label.split("T")[1].substring(0, 5); // "20:00"
          formattedLabel = `${formattedDate} ${timePart}`;
        } else {
          formattedLabel = formattedDate;
        }
      } catch {
        formattedLabel = label;
      }
    }

    const bpmValue = typeof value === "number" && !isNaN(value) ? `${value}` : "0";

    return (
      <div className="bg-white p-2.5 rounded-[12px] shadow-[0_4px_10px_rgba(0,0,0,0.12)] border-0 text-xs text-[var(--color-brown)] font-medium">
        <div className="text-[10px] text-gray-400 mb-0.5">{formattedLabel}</div>
        <div className="text-[var(--color-orange-900)] font-bold text-[13px]">
          {bpmValue} <span className="text-[10px] font-semibold text-[var(--color-brown)]">BPM</span>
        </div>
      </div>
    );
  }
  return null;
};


export default function HeartChartToggle({ horasData, diasData }: Props) {
  const [activeTab, setActiveTab] = useState<"horas" | "dias">("dias");

  // Se não houver nenhum dado, exibe fallback amigável
  if (horasData.length === 0 && diasData.length === 0) {
    return (
      <div className="w-full bg-[var(--color-sand-900)] rounded-[24px] p-6 shadow-md flex items-center justify-center min-h-[220px]">
        <span className="text-[var(--color-brown)] font-medium">
          Sem dados de batimentos disponíveis.
        </span>
      </div>
    );
  }

  // Se o usuário selecionou dias mas não tem dados, muda pro que tiver
  const currentTab = activeTab === "dias" && diasData.length === 0 ? "horas" : activeTab;

  // Cálculo dinâmico dos limites de Y para o gráfico de linha (horas)
  let minY = 0;
  let maxY = 150;
  if (horasData.length > 0) {
    const values = horasData.map((d) => d.bpm);
    const minValue = Math.min(...values);
    const maxValue = Math.max(...values);
    minY = Math.max(0, Math.floor(minValue / 10) * 10 - 10);
    maxY = Math.ceil((maxValue + 1) / 10) * 10 + 10;
  }

  // Formatação de data/hora no eixo X do gráfico de linha
  const formatXAxis = (tickItem: string) => {
    try {
      if (!tickItem || typeof tickItem !== "string") return tickItem;
      if (tickItem.includes("-") && tickItem.length >= 10) {
        const baseDate = tickItem.split("T")[0].split(" ")[0]; // "2025-10-17"
        const parts = baseDate.split("-");
        const formattedDate = parts.length >= 3 ? `${parts[2]}/${parts[1]}` : tickItem;

        // Se houver hora no timestamp
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
    <div className="w-full bg-[var(--color-sand-900)] rounded-[24px] p-5 shadow-md flex flex-col">
      {/* Cabeçalho com Título e Seletor de Abas */}
      <div className="flex flex-row justify-between items-center mb-6 w-full gap-2">
        <h3 className="text-[var(--color-orange-900)] font-bold text-[14px] leading-tight">
          {currentTab === "horas"
            ? "Batimentos - Últimas 5 horas"
            : "Média dos últimos 5 dias"}
        </h3>

        {/* Pill Selector com micro-animação */}
        <div className="flex bg-[rgba(117,72,25,0.08)] p-0.5 rounded-full border border-[rgba(117,72,25,0.1)] shrink-0">
          {diasData.length > 0 && (
            <button
              onClick={() => setActiveTab("dias")}
              className={`px-3 py-1 text-[11px] font-bold rounded-full cursor-pointer transition-all duration-300 ${
                currentTab === "dias"
                  ? "bg-[var(--color-orange-900)] text-white shadow-sm"
                  : "text-[var(--color-brown)] hover:opacity-80"
              }`}
            >
              Dias
            </button>
          )}
          {horasData.length > 0 && (
            <button
              onClick={() => setActiveTab("horas")}
              className={`px-3 py-1 text-[11px] font-bold rounded-full cursor-pointer transition-all duration-300 ${
                currentTab === "horas"
                  ? "bg-[var(--color-orange-900)] text-white shadow-sm"
                  : "text-[var(--color-brown)] hover:opacity-80"
              }`}
            >
              Horas
            </button>
          )}
        </div>
      </div>

      {/* Gráfico Ativo */}
      <div className="w-full h-[210px]">
        <ResponsiveContainer width="100%" height="100%">
          {currentTab === "horas" ? (
            <AreaChart
              data={horasData}
              margin={{
                top: 5,
                right: 10,
                left: -22,
                bottom: 5,
              }}
            >
              <defs>
                <linearGradient id="colorBpmToggle" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="var(--color-orange-900)" stopOpacity={0.2} />
                  <stop offset="95%" stopColor="var(--color-orange-900)" stopOpacity={0.0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="rgba(117, 72, 25, 0.15)" />
              <XAxis
                dataKey="data"
                axisLine={false}
                tickLine={false}
                tick={{ fill: "var(--color-brown)", fontSize: 10, fontWeight: 500 }}
                tickFormatter={formatXAxis}
                dy={10}
              />
              <YAxis
                domain={[minY, maxY]}
                axisLine={false}
                tickLine={false}
                tick={{ fill: "var(--color-brown)", fontSize: 11 }}
              />
              <Tooltip
                cursor={{ stroke: "var(--color-orange-900)", strokeWidth: 1, strokeDasharray: "3 3" }}
                content={<CustomTooltip />}
              />
              <Area
                type="monotone"
                dataKey="bpm"
                stroke="var(--color-orange-900)"
                strokeWidth={3}
                fillOpacity={1}
                fill="url(#colorBpmToggle)"
                activeDot={{ r: 6, fill: "var(--color-orange-900)", strokeWidth: 2, stroke: "#fff" }}
                dot={{ r: 3.5, fill: "var(--color-orange-900)", strokeWidth: 1.5, stroke: "#fff" }}
              />
            </AreaChart>
          ) : (
            <BarChart
              data={diasData}
              margin={{
                top: 5,
                right: 5,
                left: -22,
                bottom: 5,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="rgba(117, 72, 25, 0.15)" />
              <XAxis
                dataKey="data"
                axisLine={false}
                tickLine={false}
                tick={{ fill: "var(--color-brown)", fontSize: 11 }}
                dy={10}
              />
              <YAxis
                axisLine={false}
                tickLine={false}
                tick={{ fill: "var(--color-brown)", fontSize: 11 }}
              />
              <Tooltip
                cursor={{ fill: "rgba(191, 73, 4, 0.08)" }}
                content={<CustomTooltip />}
              />
              <Bar
                dataKey="bpm"
                fill="var(--color-orange-900)"
                radius={[4, 4, 0, 0]}
                barSize={32}
              />
            </BarChart>
          )}
        </ResponsiveContainer>
      </div>
    </div>
  );
}
