"use client";

import { useEffect, useState } from "react";
import { FaCrosshairs, FaShieldAlt } from "react-icons/fa";

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

import MapView from "../MapScreen/MapView";
import MapActions from "../MapScreen/MapActions";
import PetAddressCard from "./PetAddressCard";
import DefineSafeAreaModal from "./DefineSafeAreaModal";

import { getUltimaLocalizacaoAnimal, LocationData } from "@/services/locationService";
import { getSafeAreaByAnimalId, SafeArea } from "@/services/safeAreaService";
import { getEnderecoAtualDoAnimal } from "@/services/mapService";
import { subscribe } from "@/services/websocketService";

interface Props {
  animalId: string;
  animalName: string;
  animalImagemUrl?: string | null;
}

export default function LocationScreen({ animalId, animalName, animalImagemUrl }: Props) {
  const [currentLocation, setCurrentLocation] = useState<LocationData | null>(null);
  const [safeArea, setSafeArea] = useState<SafeArea | null>(null);
  const [address, setAddress] = useState<string | null>(null);
  const [isFetchingAddress, setIsFetchingAddress] = useState(false);
  
  const [isOutsideSafeZone, setIsOutsideSafeZone] = useState<boolean | null>(null);
  const [distanceFromPerimeter, setDistanceFromPerimeter] = useState<number | null>(null);

  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [showDefineSafeArea, setShowDefineSafeArea] = useState(false);

  // Recalculate safe zone status whenever location or safe area changes
  useEffect(() => {
    if (currentLocation && safeArea) {
      const distance = getDistanceInMeters(
        currentLocation.latitude,
        currentLocation.longitude,
        safeArea.latitude,
        safeArea.longitude
      );
      setIsOutsideSafeZone(distance > safeArea.raio);
      setDistanceFromPerimeter(Math.max(0, distance - safeArea.raio));
    } else if (!safeArea) {
      setIsOutsideSafeZone(null);
      setDistanceFromPerimeter(null);
    }
  }, [currentLocation, safeArea]);

  // Inicializa dados (Location + SafeArea)
  const loadData = async () => {
    try {
      setIsLoading(true);
      
      const [loc, sa] = await Promise.all([
        getUltimaLocalizacaoAnimal(animalId),
        getSafeAreaByAnimalId(animalId),
      ]);

      if (loc) {
        setCurrentLocation(loc);

        // Busca endereço
        setIsFetchingAddress(true);
        const addr = await getEnderecoAtualDoAnimal(loc.latitude, loc.longitude);
        setAddress(addr);
        setIsFetchingAddress(false);
      } else {
        setError("Localização não encontrada");
      }

      if (sa) {
        setSafeArea(sa);
      } else {
        setSafeArea(null);
      }
    } catch (e) {
      setError("Erro ao carregar dados da localização");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadData();

    // WebSocket Listener
    const unsubscribe = subscribe(async (data) => {
      const payload = data.payload || data;
      const wsAnimalId = payload.animalId || payload.animal || data.animalId || data.animal;

      if (wsAnimalId !== animalId) return;

      if (payload.tipo === "localizacao" || payload.latitude !== undefined) {
        console.log("📍 LocationScreen WS:", payload);
        
        setCurrentLocation({
          latitude: payload.latitude,
          longitude: payload.longitude,
        });

        setIsFetchingAddress(true);
        const addr = await getEnderecoAtualDoAnimal(payload.latitude, payload.longitude);
        setAddress(addr);
        setIsFetchingAddress(false);
      }
    });

    return () => {
      unsubscribe();
    };
  }, [animalId]);

  const handleCenterMap = () => {
    // Apenas recarrega (o MapView tem useEffect que faz panTo automático)
    loadData();
  };

  const handleCloseDefineSafeArea = (saved: boolean) => {
    setShowDefineSafeArea(false);
    if (saved) {
      loadData(); // Recarrega para buscar o novo raio e status
    }
  };

  return (
    <div className="relative w-full h-full">
      {/* MAP VIEW */}
      {currentLocation ? (
        <MapView
          lat={currentLocation.latitude}
          lng={currentLocation.longitude}
          safeArea={
            safeArea
              ? {
                  lat: safeArea.latitude,
                  lng: safeArea.longitude,
                  radius: safeArea.raio,
                }
              : null
          }
          animalImagemUrl={animalImagemUrl || undefined}
        />
      ) : (
        <div className="w-full h-full bg-gray-100 flex items-center justify-center">
          {isLoading ? "Carregando mapa..." : "Sem dados de localização"}
        </div>
      )}

      {/* OVERLAYS */}
      
      {/* Error */}
      {error && (
        <div className="absolute top-20 left-4 right-4 bg-red-100 text-red-700 p-3 rounded-lg shadow-md z-10">
          {error}
        </div>
      )}

      {/* Address Card */}
      {!isLoading && (
        <div className="absolute top-[60px] left-4 right-4 md:left-1/2 md:right-auto md:-translate-x-1/2 md:w-full md:max-w-md z-10">
          <PetAddressCard
            petName={animalName}
            address={isFetchingAddress ? "Buscando localização..." : (address || "Endereço não encontrado")}
            isOutsideSafeZone={isOutsideSafeZone}
            distanceFromPerimeter={distanceFromPerimeter}
          />
        </div>
      )}

      {/* Action Buttons */}
      {currentLocation && !isLoading && (
        <div className="absolute left-4 right-4 md:left-auto md:right-4 z-40 bottom-[200px] sm:bottom-[160px] md:bottom-28 flex justify-between md:justify-end items-center gap-4 pointer-events-none">
          <button
            onClick={() => setShowDefineSafeArea(true)}
            className="bg-[var(--color-blue)] text-white font-semibold h-[44px] px-4 rounded-xl shadow-lg flex items-center gap-2 transition-transform active:scale-95 pointer-events-auto"
          >
            <FaShieldAlt />
            <span>Definir área segura</span>
          </button>

          <div className="pointer-events-auto flex items-center">
            <MapActions onRefresh={handleCenterMap} />
          </div>
        </div>
      )}

      {/* Loading Overlay */}
      {isLoading && (
        <div className="absolute inset-0 bg-black/20 flex items-center justify-center z-50 backdrop-blur-sm">
          <div className="bg-white p-4 rounded-full shadow-lg">
            <div className="w-8 h-8 border-4 border-orange-400 border-t-transparent rounded-full animate-spin"></div>
          </div>
        </div>
      )}

      {/* Modal FullScreen para definir área */}
      {showDefineSafeArea && currentLocation && (
        <DefineSafeAreaModal
          animalId={animalId}
          initialLocation={currentLocation}
          onClose={handleCloseDefineSafeArea}
        />
      )}
    </div>
  );
}
