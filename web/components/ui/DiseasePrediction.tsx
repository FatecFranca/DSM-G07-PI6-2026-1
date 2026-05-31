"use client";

import { FaStethoscope } from "react-icons/fa";

interface DiseasePredictionProps {
  diseaseText: string;
  descriptionText?: string | null;
}

export default function DiseasePrediction({
  diseaseText,
  descriptionText,
}: DiseasePredictionProps) {
  return (
    <div
      className="w-full max-w-md mx-auto my-6 p-10 rounded-[28px] text-center flex flex-col items-center justify-center relative overflow-hidden transition-all duration-500 hover:shadow-lg"
      style={{
        backgroundColor: "var(--color-sand-900)",
        boxShadow: "0 8px 24px rgba(117,72,25,0.15)",
      }}
    >
      {/* Elemento Decorativo no Background */}
      <div className="absolute -right-6 -bottom-6 text-[var(--color-brown)] opacity-5 pointer-events-none">
        <FaStethoscope size={140} />
      </div>

      <p className="text-[13px] font-medium leading-relaxed text-[var(--color-brown)] uppercase tracking-wider mb-8">
        Segundo suas respostas ao questionário, a nossa análise identificou
      </p>

      {/* Título do Diagnóstico */}
      <h2 className="text-[24px] font-black text-[var(--color-orange-900)] leading-tight tracking-tight px-4 animate-bounce-subtle mb-6">
        {diseaseText}
      </h2>

      {/* Descrição Adicional */}
      {descriptionText && (
        <div className="w-full bg-[var(--color-sand-100)] rounded-2xl py-3 px-5 mb-8 max-w-[280px]">
          <p className="text-[12px] font-semibold text-[var(--color-brown)] leading-normal">
            {descriptionText}
          </p>
        </div>
      )}

      {/* Divisor Visual */}
      <div className="w-12 h-1 bg-[var(--color-orange-900)] opacity-20 rounded-full mb-8" />

      {/* Aviso Médico Importante */}
      <p className="text-[13px] leading-relaxed text-[var(--color-brown)] font-medium opacity-90">
        Nossa análise tem caráter informativo e não substitui uma visita ao médico veterinário. 🐾
      </p>
    </div>
  );
}
