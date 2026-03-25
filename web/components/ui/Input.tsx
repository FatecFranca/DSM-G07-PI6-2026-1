"use client";

import { useState } from "react";

type InputSize = "small" | "medium" | "large";

interface InputProps {
  label?: string;
  hintText: string;
  size?: InputSize;
  icon?: React.ReactNode;
  onChange?: (value: string) => void;
  type?: string;
  value?: string;
  centerText?: boolean;
  suffixText?: string;
}

export default function Input({
  label,
  hintText,
  size = "large",
  icon,
  onChange,
  type = "text",
  value,
  centerText = false,
  suffixText,
}: InputProps) {
  const [isFocused, setIsFocused] = useState(false);

  const sizeStyles = {
    small: {
      label: "text-xs",
      input: "text-xs",
      icon: "text-[18px]",
      paddingY: "py-3",
    },
    medium: {
      label: "text-sm",
      input: "text-sm",
      icon: "text-[20px]",
      paddingY: "py-3.5",
    },
    large: {
      label: "text-base",
      input: "text-base",
      icon: "text-[22px]",
      paddingY: "py-2.5",
    },
  };

  const currentSize = sizeStyles[size];

  return (
    <div
      className={`flex flex-col ${
        centerText ? "items-center text-center" : "items-start"
      }`}
    >

      {centerText ? (
        <div className="flex flex-col items-center gap-2">
          {icon && (
            <span className={`text-primary ${currentSize.icon}`}>
              {icon}
            </span>
          )}
          {label && (
            <span className={`text-zinc-600 ${currentSize.label}`}>
              {label}
            </span>
          )}
        </div>
      ) : (
        <div className="flex items-center gap-2">
          {icon && (
            <span className={`text-primary ${currentSize.icon}`}>
              {icon}
            </span>
          )}
          {label && (
            <span className={`text-[var(--color-foreground)] ${currentSize.label}`}>
              {label}
            </span>
          )}
        </div>
      )}

      <div className="h-2" />

      <div
        className={`
          flex items-center
          rounded-full
          border
          transition-all duration-200
          px-6
          ${
            isFocused
              ? "border-[2.5px] border-[var(--color-primary)]"
              : "border-2 border-[var(--color-primary)]"
          }
        `}
      >
        <input
          type={type}
          value={value}
          onChange={(e) => onChange?.(e.target.value)}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          placeholder={hintText}
          className={`
            bg-transparent
            outline-none
            ${currentSize.input}
            ${currentSize.paddingY}
            text-[var(--color-foreground)]
            placeholder:text-zinc-400
            ${
              centerText
                ? "text-center"
                : "text-left"
            }
          `}
        />

        {suffixText && (
          <span className={`ml-2 ${currentSize.input}`}>
            {suffixText}
          </span>
        )}
      </div>
    </div>
  );
}