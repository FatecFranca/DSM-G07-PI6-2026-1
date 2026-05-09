"use client";

interface MapActionsProps {
  onRefresh: () => void | Promise<void>;
}

export default function MapActions({ onRefresh }: MapActionsProps) {
  return (
    <div className="flex flex-col gap-2">
      <button
        onClick={onRefresh}
        className="bg-[var(--color-primary)] text-white p-3 rounded-xl shadow flex items-center justify-center"
      >
        {/* Ícone location-crosshairs */}
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="w-5 h-5 text-white"
          viewBox="0 0 512 512"
          fill="currentColor"
        >
          <path d="M256 0c-13.3 0-24 10.7-24 24V48C132.3 58.6 58.6 132.3 48 232H24c-13.3 0-24 10.7-24 24s10.7 24 24 24H48c10.6 99.7 84.3 173.4 184 184v24c0 13.3 10.7 24 24 24s24-10.7 24-24V464c99.7-10.6 173.4-84.3 184-184h24c13.3 0 24-10.7 24-24s-10.7-24-24-24H464c-10.6-99.7-84.3-173.4-184-184V24c0-13.3-10.7-24-24-24zm0 96c88.4 0 160 71.6 160 160s-71.6 160-160 160s-160-71.6-160-160s71.6-160 160-160zm0 64a96 96 0 1 0 0 192a96 96 0 1 0 0-192z" />
        </svg>
      </button>
    </div>
  );
}