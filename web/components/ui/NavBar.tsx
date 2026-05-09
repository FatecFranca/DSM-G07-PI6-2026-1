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
    <div className="w-full bg-[var(--color-sand-900)]">
      
      <div className="flex justify-around items-center h-[70px] sm:h-[85px] px-2 sm:max-w-3xl sm:mx-auto">
        
        {items.map((item, index) => {
          const isSelected = currentIndex === index;

          return (
            <div
              key={index}
              onClick={() => onChange(index)}
              className="flex flex-col items-center justify-center flex-1 cursor-pointer"
            >
              <div
                className={`text-[28px] ${
                  isSelected ? "text-[#BF4904]" : "text-[#D89042]"
                }`}
              >
                {item.icon}
              </div>

              <span
                className={`text-xs ${
                  isSelected ? "text-[#BF4904] font-bold" : "text-[#D89042]"
                }`}
              >
                {item.label}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}