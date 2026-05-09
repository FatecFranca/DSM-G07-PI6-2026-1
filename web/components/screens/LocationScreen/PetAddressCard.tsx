"use client";

import { FaMapMarkerAlt, FaCheckCircle, FaExclamationTriangle } from "react-icons/fa";

interface Props {
  petName: string;
  address: string;
  isOutsideSafeZone?: boolean | null;
  distanceFromPerimeter?: number | null;
}

export default function PetAddressCard({
  petName,
  address,
  isOutsideSafeZone,
}: Props) {
  const showSafeZoneStatus = isOutsideSafeZone !== null && isOutsideSafeZone !== undefined;
  const isInSafeZone = isOutsideSafeZone === false;

  return (
    <div className="w-full py-5 px-6 bg-[var(--color-sand-100)] rounded-[24px] shadow-[0_3px_6px_rgba(0,0,0,0.1)] flex flex-col">
      <div className="flex justify-center items-center gap-2 mb-2.5">
        <FaMapMarkerAlt className="text-[var(--color-primary)] text-[22px]" />
        <h3 className="text-[var(--color-primary)] font-bold text-[16px] uppercase truncate">
          {petName} ESTÁ EM:
        </h3>
      </div>
      
      <p className="text-center text-[var(--color-brown)] text-[15px] leading-[1.4]">
        {address}
      </p>

      {showSafeZoneStatus && (
        <div
          className={`mt-4 py-3 px-4 rounded-2xl border-[1.5px] flex items-center justify-center gap-2 ${
            isInSafeZone
              ? "bg-[var(--color-green-50)] border-[var(--color-green-200)]"
              : "bg-[var(--color-red-50)] border-[var(--color-red-200)]"
          }`}
        >
          {isInSafeZone ? (
            <FaCheckCircle className="text-[var(--color-green-700)] text-[20px]" />
          ) : (
            <FaExclamationTriangle className="text-[var(--color-red-700)] text-[20px]" />
          )}
          <span
            className={`font-semibold text-[14px] text-center ${
              isInSafeZone ? "text-[var(--color-green-700)]" : "text-[var(--color-red-700)]"
            }`}
          >
            {isInSafeZone ? "Pet dentro da área segura" : "Pet fora da área segura"}
          </span>
        </div>
      )}
    </div>
  );
}
