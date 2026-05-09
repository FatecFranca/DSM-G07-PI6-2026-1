"use client";

import { useState } from "react";
import Image from "next/image";
import {
  FaMars,
  FaVenus,
  FaHeartbeat,
  FaBatteryFull,
  FaChevronUp,
  FaChevronDown,
} from "react-icons/fa";

interface StatusBarProps {
  isConnected: boolean;
  animalName?: string;
  sex?: "M" | "F";
  lastBpm?: number;
  battery?: number;
}

export default function StatusBar({
  isConnected,
  animalName = "Pet",
  sex = "M",
  lastBpm,
  battery = 96,
}: StatusBarProps) {

  const [isExpanded, setIsExpanded] = useState(false);

  function toggle() {
    setIsExpanded(!isExpanded);
  }

  return (
    <div
      className={`
        w-full
        bg-[var(--color-sand-100)]
        rounded-t-[30px]
        p-4
        flex flex-col
        transition-all duration-300
        ${isExpanded ? "h-[220px]" : "h-[110px]"}
      `}
    >
      <div className="h-[28px] flex items-center justify-center mb-2">
        <div
          onClick={toggle}
          className="w-[80px] h-[24px] rounded-full bg-[var(--color-sand-900)] border border-[var(--color-sand-900)] flex items-center justify-center cursor-pointer"
        >
          {isExpanded ? (
            <FaChevronDown className="text-[var(--color-orange-900)] text-xs" />
          ) : (
            <FaChevronUp className="text-[var(--color-orange-900)] text-xs" />
          )}
        </div>
      </div>

      <div className="flex justify-between items-center flex-1">
        <div className="flex items-center gap-3">
          <div className="w-[50px] h-[50px] rounded-full overflow-hidden bg-[var(--color-sand-200)]">
            <Image
              src="/images/uno.png"
              alt="Pet"
              width={50}
              height={50}
              className="object-cover w-full h-full"
              loading="eager"
            />
          </div>

          <div className="flex flex-col justify-center">
            <div className="flex items-center gap-2">
              <h2 className="text-lg font-bold text-[var(--color-orange-900)]">
                {animalName}
              </h2>

              {sex === "M" ? (
                <FaMars className="text-[var(--color-orange-900)] text-lg" />
              ) : (
                <FaVenus className="text-[var(--color-orange-900)] text-lg" />
              )}
            </div>

            <div className="flex items-center gap-2 mt-1">
              <span className="text-xs text-[var(--color-brown)]">
                {isConnected ? "Conectado" : "Desconectado"}
              </span>

              <div
                className={`w-2 h-2 rounded-full ${
                  isConnected ? "bg-green-500" : "bg-red-500"
                }`}
              />
            </div>
          </div>
        </div>

        <div className="flex flex-col items-end justify-center">
          <div className="flex items-center gap-2">
            <span className="text-3xl font-bold text-[var(--color-brown)]">
              {lastBpm ?? "--"}
            </span>

            <FaHeartbeat className="text-[var(--color-orange-400)] text-lg" />

            <span className="text-sm font-semibold text-[var(--color-brown)]">
              BPM
            </span>
          </div>

          <div className="flex items-center gap-2 mt-1">
            <FaBatteryFull className="text-green-500 text-sm" />

            <span className="text-sm text-[var(--color-brown)] font-semibold">
              {battery}%
            </span>
          </div>
        </div>
      </div>

      {isExpanded && (
        <div className="mt-3 text-center text-sm text-[var(--color-brown)]">
          Mais informações em breve...
        </div>
      )}
    </div>
  );
}