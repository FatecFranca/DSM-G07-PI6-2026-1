"use client";

import { FaHome, FaHeartbeat, FaStethoscope, FaMapMarkerAlt } from "react-icons/fa";

interface NavBarProps {
  currentIndex: number;
  onChange: (index: number) => void;
}

export default function NavBar({ currentIndex, onChange }: NavBarProps) {
  const items = [
    { icon: <FaHome />, label: "Início" },
    { icon: <FaHeartbeat />, label: "Saúde" },
    { icon: <FaStethoscope />, label: "Checkup" },
    { icon: <FaMapMarkerAlt />, label: "Localização" },
  ];

  return (
    <div className="fixed bottom-0 left-0 w-full bg-[var(--background)] h-[85px] px-2 pt-1 pb-3 flex justify-between px-80">
      {items.map((item, index) => {
        const isSelected = currentIndex === index;

        return (
          <div
            key={index}
            onClick={() => onChange(index)}
            className="flex flex-col items-center justify-center flex-1 cursor-pointer"
          >
            <div
              className={`text-[30px] ${
                isSelected
                  ? "text-[var(--color-primary-active)]"
                  : "text-orange-300"
              }`}
            >
              {item.icon}
            </div>

            <span
              className={`text-xs mt-1 ${
                isSelected
                  ? "text-[var(--color-primary-active)] font-bold"
                  : "text-orange-300"
              }`}
            >
              {item.label}
            </span>
          </div>
        );
      })}
    </div>
  );
}