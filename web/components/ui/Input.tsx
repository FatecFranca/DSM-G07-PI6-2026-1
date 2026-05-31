"use client";

import { useState } from "react";
import { FaEye, FaEyeSlash } from "react-icons/fa";

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
  textColor?: string;
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
  textColor,
}: InputProps) {
  const [isFocused, setIsFocused] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const isPasswordType = type === "password";
  const inputType = isPasswordType ? (showPassword ? "text" : "password") : type;

  const sizeStyles = {
    small: {
      label: "text-xs",
      input: "text-xs w-full",
      icon: "text-[18px]",
      paddingY: "py-3",
    },
    medium: {
      label: "text-sm",
      input: "text-sm w-full",
      icon: "text-[20px]",
      paddingY: "py-3.5",
    },
    large: {
      label: "text-base",
      input: "text-base w-full",
      icon: "text-[22px]",
      paddingY: "py-2.5",
    },
  };

  const currentSize = sizeStyles[size];

  return (
    <div
      className={`w-full flex flex-col ${
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
          w-full
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
          type={inputType}
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
            ${textColor || "text-[var(--color-foreground)]"}
            ${textColor ? "placeholder:text-[var(--color-brown)] placeholder:opacity-60" : "placeholder:text-zinc-400"}
            ${
              centerText
                ? "text-center"
                : "text-left"
            }
          `}
        />

        {isPasswordType && (
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="ml-2 text-[var(--color-primary)] hover:text-[var(--color-primary-active)] transition-colors focus:outline-none cursor-pointer"
          >
            {showPassword ? <FaEyeSlash className="text-lg" /> : <FaEye className="text-lg" />}
          </button>
        )}

        {suffixText && (
          <span className={`ml-2 ${currentSize.input} ${textColor || "text-[var(--color-foreground)]"}`}>
            {suffixText}
          </span>
        )}
      </div>
    </div>
  );
}