"use client";

import { useEffect, useState } from "react";
import { animalStatsService, AnaliseBatimento } from "@/services/animalStatsService";
import { subscribe } from "@/services/websocketService";

interface Props {
  animalId: string;
}

export default function HealthStatsCard({ animalId }: Props) {
  const [analise, setAnalise] = useState<AnaliseBatimento | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadAnalise = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await animalStatsService.getAnaliseUltimoBatimento(animalId);
      setAnalise(data);
    } catch (err) {
      setError("Não foi possível carregar a análise no momento.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadAnalise();

    const unsubscribe = subscribe((data) => {
      const payload = data.payload || data;
      const wsAnimalId = payload.animalId || payload.animal || data.animalId || data.animal;
      if (wsAnimalId === animalId && (payload.tipo === "batimento" || payload.frequenciaMedia !== undefined)) {
        loadAnalise();
      }
    });

    return () => {
      unsubscribe();
    };
  }, [animalId]);

  return (
    <div className="w-full bg-[var(--color-sand-900)] rounded-[24px] p-6 shadow-md flex flex-col items-center">
      <h3 className="text-[var(--color-orange-900)] font-bold text-[22px] text-center mb-4">
        Análise de batimentos
      </h3>

      {isLoading && !analise ? (
        <div className="flex items-center justify-center h-[120px]">
          <div className="w-6 h-6 border-2 border-[var(--color-primary)] border-t-transparent rounded-full animate-spin"></div>
        </div>
      ) : error && !analise ? (
        <div className="flex items-center justify-center h-[120px] text-red-500 font-semibold text-center text-[14px]">
          {error}
        </div>
      ) : !analise ? (
        <div className="flex items-center justify-center h-[120px] text-[var(--color-brown)] text-[14px]">
          Nenhuma análise disponível.
        </div>
      ) : (
        <>
          <p className="font-bold text-[16px] text-[var(--color-brown)] text-center mb-4">
            {analise.titulo}
          </p>
          
          <p className="text-[14px] text-[var(--color-brown)] text-center leading-relaxed mb-5">
            {analise.interpretacao}
          </p>

          <h4 className="text-[var(--color-orange-900)] font-bold text-[16px] text-center mb-1">
            Valor do batimento:
          </h4>
          <span className="text-[var(--color-brown)] font-black text-[28px] tracking-tight">
            {analise.batimentoAnalisado} BPM
          </span>
        </>
      )}
    </div>
  );
}
