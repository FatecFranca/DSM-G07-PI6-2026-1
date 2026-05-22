"use client";

import { useState, useEffect } from "react";
import { animalStatsService } from "@/services/animalStatsService";
import { subscribe } from "@/services/websocketService";

interface Props {
  animalId: string;
}

export default function HeartDateCard({ animalId }: Props) {
  const [date, setDate] = useState<string>(new Date().toISOString().split("T")[0]);
  const [bpm, setBpm] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [mensagemApi, setMensagemApi] = useState<string | null>(null);

  const fetchMediaData = async (selectedDate: string) => {
    if (!selectedDate) {
      setBpm(null);
      setMensagemApi(null);
      return;
    }

    setIsLoading(true);
    setError(null);
    setMensagemApi(null);
    
    try {
      const result = await animalStatsService.getMediaPorData(animalId, selectedDate);
      if (result !== null) {
        setBpm(result);
      } else {
        setMensagemApi("Nenhum dado encontrado para o intervalo fornecido.");
        setBpm(null);
      }
    } catch (err) {
      setError("Erro ao buscar dados.");
      setBpm(null);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchMediaData(date);

    const unsubscribe = subscribe((data) => {
      const payload = data.payload || data;
      const wsAnimalId = payload.animalId || payload.animal || data.animalId || data.animal;
      if (wsAnimalId === animalId && (payload.tipo === "batimento" || payload.frequenciaMedia !== undefined)) {
        fetchMediaData(date);
      }
    });

    return () => unsubscribe();
  }, [animalId, date]);

  const handleDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setDate(e.target.value);
  };

  return (
    <div className="w-full bg-[var(--color-sand-900)] rounded-[24px] p-6 shadow-md flex flex-col items-center">
      <h3 className="text-[var(--color-orange-900)] font-bold text-[22px] text-center mb-4">
        Média de batimento cardíaco por data
      </h3>
      
      <h4 className="text-[var(--color-orange-900)] font-semibold text-[16px] text-center mb-2">
        Selecione uma data:
      </h4>
      <div className="w-full max-w-[200px] mb-6 relative">
        <input
          type="date"
          value={date}
          onChange={handleDateChange}
          className="w-full bg-black/5 text-[var(--color-brown)] font-semibold rounded-full px-4 py-2 outline-none text-center focus:ring-2 focus:ring-[var(--color-primary)]/50 appearance-none transition-all cursor-pointer"
        />
      </div>

      <h4 className="text-[var(--color-orange-900)] font-semibold text-[16px] text-center mb-2">
        Resultado:
      </h4>

      <div className="flex items-center justify-center min-h-[40px]">
        {isLoading ? (
          <div className="w-6 h-6 border-2 border-[var(--color-primary)] border-t-transparent rounded-full animate-spin"></div>
        ) : error ? (
          <span className="text-red-500 text-[14px] font-medium text-center leading-relaxed">{error}</span>
        ) : bpm !== null ? (
          <span className="text-[var(--color-brown)] font-black text-[28px] tracking-tight">
            {bpm} BPM
          </span>
        ) : mensagemApi ? (
          <span className="text-[var(--color-brown)] text-[14px] font-medium text-center leading-relaxed">
            {mensagemApi}
          </span>
        ) : (
          <span className="text-[var(--color-brown)] text-[14px] font-medium text-center leading-relaxed">
            Sem dados
          </span>
        )}
      </div>
    </div>
  );
}
