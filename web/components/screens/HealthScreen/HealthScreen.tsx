"use client";

import { useEffect, useState } from "react";
import { subscribe } from "@/services/websocketService";
import { animalStatsService, HeartbeatData } from "@/services/animalStatsService";

import HeartChartToggle from "./HeartChartToggle";
import HeartDateCard from "./HeartDateCard";
import HealthStatsCard from "./HealthStatsCard";


interface Props {
  animalId: string;
  animalName: string;
}

export default function HealthScreen({ animalId, animalName }: Props) {
  const [medias5Dias, setMedias5Dias] = useState<HeartbeatData[]>([]);
  const [medias5Horas, setMedias5Horas] = useState<HeartbeatData[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadData = async () => {
    try {
      const [dias, horas] = await Promise.all([
        animalStatsService.getMediaUltimos5Dias(animalId),
        animalStatsService.getMediaUltimas5HorasRegistradas(animalId),
      ]);
      setMedias5Dias(dias);
      setMedias5Horas(horas);
    } catch (err) {
      setError("Erro ao carregar dados dos gráficos.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    setIsLoading(true);
    loadData();

    // Listener do WebSocket para recarregar as médias
    const unsubscribe = subscribe((data) => {
      const payload = data.payload || data;
      const wsAnimalId = payload.animalId || payload.animal || data.animalId || data.animal;

      if (wsAnimalId === animalId) {
        if (payload.tipo === "batimento" || payload.frequenciaMedia !== undefined) {
          console.log("❤️ [HealthScreen] Novo batimento recebido, recarregando gráficos...");
          loadData();
        }
      }
    });

    return () => {
      unsubscribe();
    };
  }, [animalId]);

  return (
    <div className="w-full h-full overflow-y-auto bg-[var(--color-sand-100)] px-4 py-6 pb-[250px] scrollbar-hide">
      <div className="flex flex-col items-center max-w-md mx-auto">
        <h2 className="text-[var(--color-orange-900)] text-[24px] font-bold mb-2">
          Painel de Saúde
        </h2>
        
        <p className="text-[14px] text-[var(--color-brown)] text-center mb-8 px-2 font-medium">
          Frequência cardíaca, padrões de atividade e informações de saúde reunidas em um só lugar.
          <br />
          Tenha controle total da saúde do seu pet.
        </p>

        {isLoading ? (
          <div className="flex items-center justify-center w-full h-[220px]">
             <div className="w-8 h-8 border-4 border-[var(--color-orange-900)] border-t-transparent rounded-full animate-spin"></div>
          </div>
        ) : error ? (
          <div className="w-full bg-[var(--color-sand-900)] p-4 rounded-[24px] mb-5 shadow-md">
            <p className="text-red-600 font-semibold text-center">{error}</p>
          </div>
        ) : medias5Dias.length === 0 && medias5Horas.length === 0 ? (
          <div className="w-full bg-[var(--color-sand-900)] py-6 px-4 rounded-[24px] mb-5 shadow-md">
            <p className="text-[var(--color-brown)] font-medium text-center">
              Sem dados dos últimos dias para exibir no gráfico.
            </p>
          </div>
        ) : (
          <div className="w-full mb-5">
            <HeartChartToggle
              horasData={medias5Horas}
              diasData={medias5Dias}
            />
          </div>
        )}

        <div className="w-full mb-5">
          <HeartDateCard animalId={animalId} />
        </div>

        <div className="w-full mb-10">
          <HealthStatsCard animalId={animalId} />
        </div>
      </div>
    </div>
  );
}
