"use client";

import Image from "next/image";

interface StatusBarProps {
  isConnected: boolean;
  animalName?: string;
}

export default function StatusBar({
  isConnected,
  animalName = "Pet",
}: StatusBarProps) {
  return (
    <div
      className="
        w-full
        bg-[var(--color-sand-100)]
        rounded-t-[30px]
        p-4
        h-[110px]
        flex flex-col justify-between
      "
    >
      {/* LINHA DE CIMA */}
      <div className="flex items-center justify-between">
        
        {/* ESQUERDA: FOTO + NOME */}
        <div className="flex items-center gap-3">
          
          {/* FOTO (CircleAvatar) */}
          <div className="w-[50px] h-[50px] rounded-full overflow-hidden bg-[var(--color-sand-200)]">
            <Image
              src="/images/uno.png"
              alt="Pet"
              width={50}
              height={50}
              className="object-cover w-full h-full"
            />
          </div>

          {/* NOME */}
          <h2 className="text-lg font-bold text-[var(--color-orange-900)]">
            {animalName}
          </h2>
        </div>

        {/* STATUS */}
        <div className="flex items-center gap-2">
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

      {/* LINHA DE BAIXO */}
      <div className="flex items-end justify-between">
        <div className="flex items-end gap-1">
          <span className="text-3xl font-bold text-[var(--color-brown)]">
            72
          </span>
          <span className="text-sm text-[var(--color-brown)] mb-1">
            BPM
          </span>
        </div>

        <div className="w-[80px] h-[30px] bg-black/5 rounded-md" />
      </div>
    </div>
  );
}