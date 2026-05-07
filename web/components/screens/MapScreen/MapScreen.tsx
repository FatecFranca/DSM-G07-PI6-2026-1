"use client";

import { useEffect, useState } from "react";
import MapView from "./MapView";
import MapOverlay from "./MapOverlay";
import MapActions from "./MapActions";
import { getUltimaLocalizacaoAnimal } from "@/services/locationService";
import { authService } from "@/services/authService";
import {
  connectWebSocket,
  subscribe,
} from "@/services/websocketService";

interface MapScreenProps {
  setLastBpm: (bpm: number) => void;
}

export default function MapScreen({
  setLastBpm,
}: MapScreenProps) {
  const [isLoaded, setIsLoaded] = useState(false);
  const [isLoadingLocation, setIsLoadingLocation] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isOutsideSafeZone, setIsOutsideSafeZone] = useState(false);

  const [lat, setLat] = useState<number | null>(null);
  const [lng, setLng] = useState<number | null>(null);

  const animalId = "68194120636f719fcd5ee5fd";

  async function loadLocation() {
    try {
      setIsLoadingLocation(true);
      setError(null);

      console.log("📡 Buscando localização inicial...");

      const location = await getUltimaLocalizacaoAnimal(animalId);

      console.log("📍 Localização recebida API:", location);

      if (!location) {
        setError("Nenhuma localização encontrada");
        return;
      }

      setLat(location.latitude);
      setLng(location.longitude);

      setIsOutsideSafeZone(false);
    } catch (e) {
      console.error("❌ Erro loadLocation:", e);

      setError("Erro ao carregar localização");
    } finally {
      setIsLoadingLocation(false);
    }
  }

  useEffect(() => {
    async function init() {
      try {
        console.log("🚀 Iniciando MapScreen...");

        authService.init();

        if (!authService.isAuthenticated()) {
          console.log("🔐 Fazendo login...");

          await authService.login(
            "henriquealmeidaflorentino@gmail.com",
            "senha123"
          );
        }

        console.log("🔑 Token carregado");

        connectWebSocket();

        subscribe((data) => {
          console.log("📩 WS RAW:", data);

          const wsAnimalId =
            data.animalId ||
            data.animal ||
            data?.payload?.animal;

          console.log("🆔 Animal WS:", wsAnimalId);
          console.log("🆔 Animal esperado:", animalId);

          if (wsAnimalId !== animalId) {
            console.log("⛔ Ignorado por animalId diferente");
            return;
          }

          // LOCALIZAÇÃO
          if (
            data.tipo === "localizacao" ||
            data.latitude
          ) {
            console.log("📍 Atualizando mapa realtime");

            setLat(data.latitude);
            setLng(data.longitude);
          }

          // BATIMENTO
          if (
            data.tipo === "batimento" ||
            data.frequenciaMedia
          ) {
            console.log(
              "❤️ BPM atualizado realtime:",
              data.frequenciaMedia
            );

            setLastBpm(data.frequenciaMedia);
          }
        });

        await loadLocation();
      } catch (e) {
        console.error("❌ Erro init:", e);

        setError("Erro ao inicializar");
        setIsLoadingLocation(false);
      }
    }

    init();
  }, []);

  return (
    <div className="w-full h-screen relative overflow-hidden">
      {lat && lng && (
        <MapView
          lat={lat}
          lng={lng}
          onMapLoaded={() => setIsLoaded(true)}
        />
      )}

      <MapOverlay
        isLoaded={isLoaded}
        isLoadingLocation={isLoadingLocation}
        error={error}
        isOutsideSafeZone={isOutsideSafeZone}
      />

      <div className="absolute right-4 z-40 bottom-[200px] sm:bottom-[160px] md:bottom-28">
        <MapActions onRefresh={loadLocation} />
      </div>
    </div>
  );
}