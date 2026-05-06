"use client";

import { useEffect, useState } from "react";
import MapView from "./MapView";
import MapOverlay from "./MapOverlay";
import MapActions from "./MapActions";
import {
  getUltimaLocalizacaoAnimal,
} from "@/services/locationService";
import { authService } from "@/services/authService";

export default function MapScreen() {
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

      const location = await getUltimaLocalizacaoAnimal(animalId);

      if (!location) {
        setError("Nenhuma localização encontrada");
        return;
      }

      setLat(location.latitude);
      setLng(location.longitude);

      // 🔜 depois vamos calcular área segura aqui
      setIsOutsideSafeZone(false);

    } catch {
      setError("Erro ao carregar localização");
    } finally {
      setIsLoadingLocation(false);
    }
  }

  useEffect(() => {
    async function init() {
      try {
        authService.init();

        if (!authService.isAuthenticated()) {
          await authService.login(
            "henriquealmeidaflorentino@gmail.com",
            "senha123"
          );
        }

        await loadLocation();
      } catch (e) {
        console.error("Erro init:", e);
        setError("Erro ao inicializar");
        setIsLoadingLocation(false);
      }
    }

    init();
  }, []);

  return (
    <div className="w-full h-screen relative overflow-hidden">
      
      {/* MAPA */}
      {lat && lng && (
        <MapView
          lat={lat}
          lng={lng}
          onMapLoaded={() => setIsLoaded(true)}
        />
      )}

      {/* OVERLAY */}
      <MapOverlay
        isLoaded={isLoaded}
        isLoadingLocation={isLoadingLocation}
        error={error}
        isOutsideSafeZone={isOutsideSafeZone}
      />

      {/* AÇÕES */}
      <div className="absolute right-4 z-40 bottom-[200px] sm:bottom-[160px] md:bottom-28">
        <MapActions onRefresh={loadLocation} />
      </div>
    </div>
  );
}