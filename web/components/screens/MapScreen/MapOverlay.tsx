"use client";

import { FaCheckCircle, FaExclamationTriangle } from "react-icons/fa";

interface Props {
  isLoaded: boolean;
  isLoadingLocation: boolean;
  error: string | null;
  isOutsideSafeZone: boolean | null;
}

export default function MapOverlay({
  isLoaded,
  isLoadingLocation,
  error,
  isOutsideSafeZone,
}: Props) {
  return (
    <>
      {/* LOADING */}
      {(!isLoaded || isLoadingLocation) && (
        <div className="absolute inset-0 bg-black/30 flex items-center justify-center z-50">
          <span className="text-white">Carregando mapa...</span>
        </div>
      )}

      {/* ERRO */}
      {error && (
        <div className="absolute top-24 left-4 right-4 bg-red-100 p-4 rounded z-50">
          {error}
        </div>
      )}

      {/* SAFE ZONE NOTIFICATION */}
      {isOutsideSafeZone === true && (
        <div className="absolute top-4 right-4 z-50">
          <div
            className="py-2 px-3 rounded-xl border-[1.5px] flex items-center gap-2 shadow-md bg-[var(--color-red-50)] border-[var(--color-red-200)]"
          >
            <FaExclamationTriangle className="text-[var(--color-red-700)] text-[18px]" />
            <span
              className="font-semibold text-[13px] text-[var(--color-red-700)]"
            >
              Pet fora da área segura
            </span>
          </div>
        </div>
      )}
    </>
  );
}