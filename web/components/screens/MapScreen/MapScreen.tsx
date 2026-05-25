"use client";

import { useEffect, useState } from "react";
import { FaSignOutAlt } from "react-icons/fa";
import MapView from "./MapView";
import MapOverlay from "./MapOverlay";
import MapActions from "./MapActions";
import { getUltimaLocalizacaoAnimal } from "@/services/locationService";
import { getSafeAreaByAnimalId, SafeArea } from "@/services/safeAreaService";
import {
  connectWebSocket,
  subscribe,
} from "@/services/websocketService";

function getDistanceInMeters(lat1: number, lon1: number, lat2: number, lon2: number) {
  const R = 6371e3;
  const rad = Math.PI / 180;
  const dLat = (lat2 - lat1) * rad;
  const dLon = (lon2 - lon1) * rad;
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1 * rad) * Math.cos(lat2 * rad) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}

interface MapScreenProps {
  setLastBpm: (bpm: number | null) => void;
  animalId: string;
  animalName: string;
  onLogout?: () => void;
}

export default function MapScreen({
  setLastBpm,
  animalId,
  animalName,
  onLogout,
}: MapScreenProps) {
  const [isLoaded, setIsLoaded] = useState(false);
  const [isLoadingLocation, setIsLoadingLocation] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isOutsideSafeZone, setIsOutsideSafeZone] = useState<boolean | null>(null);
  const [safeArea, setSafeArea] = useState<SafeArea | null>(null);

  const [lat, setLat] = useState<number | null>(null);
  const [lng, setLng] = useState<number | null>(null);

  async function loadLocation() {
    try {
      setIsLoadingLocation(true);
      setError(null);

      console.log("📡 Buscando localização inicial e área segura...");

      const [location, sa] = await Promise.all([
        getUltimaLocalizacaoAnimal(animalId),
        getSafeAreaByAnimalId(animalId)
      ]);

      console.log("📍 Localização recebida API:", location);

      if (!location) {
        setError("Nenhuma localização encontrada");
        return;
      }

      setLat(location.latitude);
      setLng(location.longitude);

      if (sa) {
        setSafeArea(sa);
      } else {
        setSafeArea(null);
      }
    } catch (e) {
      console.error("❌ Erro loadLocation:", e);

      setError("Erro ao carregar localização");
    } finally {
      setIsLoadingLocation(false);
    }
  }

  useEffect(() => {
    if (lat !== null && lng !== null && safeArea) {
      const distance = getDistanceInMeters(
        lat,
        lng,
        safeArea.latitude,
        safeArea.longitude
      );
      setIsOutsideSafeZone(distance > safeArea.raio);
    } else if (!safeArea) {
      setIsOutsideSafeZone(null);
    }
  }, [lat, lng, safeArea]);

  useEffect(() => {
    if (!animalId) return;

    let unsubscribe: (() => void) | undefined;

    async function init() {
      try {
        console.log("🚀 Iniciando MapScreen...");
        console.log("🔑 Token carregado");

        connectWebSocket(animalId);

        unsubscribe = subscribe((data) => {
          console.log("📩 WS RAW:", data);

          const payload = data.payload || data;

          const wsAnimalId =
            payload.animalId ||
            payload.animal ||
            data.animalId ||
            data.animal;

          console.log("🆔 Animal WS:", wsAnimalId);
          console.log("🆔 Animal esperado:", animalId);

          if (wsAnimalId !== animalId) {
            console.log("⛔ Ignorado por animalId diferente");
            return;
          }

          // LOCALIZAÇÃO
          if (
            payload.tipo === "localizacao" ||
            payload.latitude !== undefined
          ) {
            console.log("📍 Atualizando mapa realtime");

            setLat(payload.latitude);
            setLng(payload.longitude);

            if (payload.isOutsideSafeZone !== undefined) {
              setIsOutsideSafeZone(payload.isOutsideSafeZone);
            } else if (payload.foraDaAreaSegura !== undefined) {
              setIsOutsideSafeZone(payload.foraDaAreaSegura);
            }
          }

          // BATIMENTO
          if (
            payload.tipo === "batimento" ||
            payload.frequenciaMedia !== undefined
          ) {
            console.log(
              "❤️ BPM atualizado realtime:",
              payload.frequenciaMedia
            );

            setLastBpm(payload.frequenciaMedia);
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

    return () => {
      if (unsubscribe) {
        unsubscribe();
      }
    };
  }, [animalId]);

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

      {/* 🚪 LOGOUT BUTTON (Only on Map Screen, Floating top-right) */}
      {onLogout && (
        <button
          onClick={onLogout}
          title="Sair"
          className="fixed top-5 right-5 w-11 h-11 rounded-full bg-[var(--color-primary)] hover:brightness-110 active:scale-95 text-white flex items-center justify-center shadow-md transition-all duration-300 z-50 cursor-pointer"
        >
          <FaSignOutAlt className="text-xl" />
        </button>
      )}
    </div>
  );
}