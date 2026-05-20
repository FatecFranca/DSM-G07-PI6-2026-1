"use client";

import { useEffect, useState } from "react";

import MapScreen from "@/components/screens/MapScreen/MapScreen";
import LocationScreen from "@/components/screens/LocationScreen/LocationScreen";
import HealthScreen from "@/components/screens/HealthScreen/HealthScreen";
import BottomNavWithStatus from "@/components/ui/BottomNavWithStatus";

import { getAnimalData } from "@/services/animalService";
import { connectWebSocket, subscribe, subscribeConnection } from "@/services/websocketService";

export default function AppShell() {
  const [currentIndex, setCurrentIndex] = useState(0);

  const [lastBpm, setLastBpm] = useState<number | null>(null);
  const [isConnected, setIsConnected] = useState(false);

  const animalId = "68194120636f719fcd5ee5fd";

  useEffect(() => {
    // Inicializa a conexão do WebSocket de forma global para o animal
    connectWebSocket(animalId);

    const unsubscribeConnection = subscribeConnection((status) => {
      setIsConnected(status);
    });

    const unsubscribeTelemetry = subscribe((data) => {
      const payload = data.payload || data;
      const wsAnimalId = payload.animalId || payload.animal || data.animalId || data.animal;

      if (wsAnimalId === animalId) {
        if (payload.tipo === "batimento" || payload.frequenciaMedia !== undefined) {
          console.log("❤️ [AppShell] BPM atualizado via WS:", payload.frequenciaMedia);
          setLastBpm(payload.frequenciaMedia);
        }
      }
    });

    return () => {
      unsubscribeConnection();
      unsubscribeTelemetry();
    };
  }, []);

  useEffect(() => {
    async function loadAnimal() {
      console.log("🐶 Buscando dados animal...");

      const animal = await getAnimalData(animalId);

      console.log("📦 Resposta animal:", animal);

      if (animal?.bpm != null) {
        console.log("❤️ SETANDO BPM:", animal.bpm);

        setLastBpm(animal.bpm);
      } else {
        console.log("❌ BPM veio null/undefined");
      }
    }

    loadAnimal();
  }, []);

  const pages = [
    <MapScreen
      key="map"
      setLastBpm={setLastBpm}
    />,
    <HealthScreen
      key="health"
      animalId={animalId}
      animalName="Uno"
    />,
    <div key="checkup">Checkup</div>,
    <LocationScreen
      key="location"
      animalId={animalId}
      animalName="Uno"
    />,
  ];

  return (
    <div className="h-screen overflow-hidden">
      {pages[currentIndex]}

      <BottomNavWithStatus
        currentIndex={currentIndex}
        onChange={setCurrentIndex}
        lastBpm={lastBpm}
        isConnected={isConnected}
        animalId={animalId}
      />
    </div>
  );
}