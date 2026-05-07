"use client";

import { useEffect, useState } from "react";

import MapScreen from "@/components/screens/MapScreen/MapScreen";
import BottomNavWithStatus from "@/components/ui/BottomNavWithStatus";

import { getAnimalData } from "@/services/animalService";

export default function AppShell() {
  const [currentIndex, setCurrentIndex] = useState(0);

  const [lastBpm, setLastBpm] = useState<number | null>(null);

  const animalId = "68194120636f719fcd5ee5fd";

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
    <div key="location">Location</div>,
  ];

  return (
    <div className="h-screen overflow-hidden">
      {pages[currentIndex]}

      <BottomNavWithStatus
        currentIndex={currentIndex}
        onChange={setCurrentIndex}
        lastBpm={lastBpm}
      />
    </div>
  );
}