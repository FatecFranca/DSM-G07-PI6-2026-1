"use client";

type ButtonSize = "small" | "medium" | "large";

interface ButtonProps {
  text: string;
  onClick: () => void;
  icon?: React.ReactNode;
  size?: ButtonSize;
}

export default function Button({
  text,
  onClick,
  icon,
  size = "medium",
}: ButtonProps) {
  const sizeStyles = {
    small: "h-[40px] px-5 text-sm",
    medium: "h-[50px] px-8 text-base",
    large: "h-[60px] px-8 text-lg",
  };

  return (
    <button
      onClick={onClick}
      className={`
        flex items-center justify-center gap-2
        ${sizeStyles[size]}
        bg-[var(--color-primary)]
        active:bg-[var(--color-primary-active)]
        text-white
        font-semibold
        rounded-full
      `}
    >
      {icon && <span>{icon}</span>}
      <span>{text}</span>
    </button>
  );
}