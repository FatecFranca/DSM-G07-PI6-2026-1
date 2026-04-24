"use client";

export default function MapActions() {
  return (
    <>
      {/* botão centralizar */}
      <button className="absolute bottom-32 right-4 w-12 h-12 rounded-full bg-[var(--color-primary)] text-white">
        📍
      </button>

      {/* logout */}
      <button className="absolute top-10 right-4 w-10 h-10 rounded-full bg-[var(--color-primary)] text-white">
        ⎋
      </button>
    </>
  );
}