"use client";

import { useEffect, useState } from "react";

import MapScreen from "@/components/screens/MapScreen/MapScreen";
import LocationScreen from "@/components/screens/LocationScreen/LocationScreen";
import BottomNavWithStatus from "@/components/ui/BottomNavWithStatus";

import { getAnimalData } from "@/services/animalService";
import { subscribeConnection } from "@/services/websocketService";

export default function AppShell() {
  const [currentIndex, setCurrentIndex] = useState(0);

  const [lastBpm, setLastBpm] = useState<number | null>(null);
  const [isConnected, setIsConnected] = useState(false);

  const animalId = "68194120636f719fcd5ee5fd";

  useEffect(() => {
    const unsubscribeConnection = subscribeConnection((status) => {
      setIsConnected(status);
    });

    return () => {
      unsubscribeConnection();
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
    <div key="health">Health</div>,
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
      />
    </div>
  );
}