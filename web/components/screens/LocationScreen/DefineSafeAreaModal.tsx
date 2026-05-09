"use client";

import { useState } from "react";
import MapView from "../MapScreen/MapView";
import { createSafeArea } from "@/services/safeAreaService";
import { LocationData } from "@/services/locationService";
import { FaArrowLeft, FaInfoCircle } from "react-icons/fa";

interface Props {
  animalId: string;
  initialLocation: LocationData;
  onClose: (saved: boolean) => void;
}

export default function DefineSafeAreaModal({
  animalId,
  initialLocation,
  onClose,
}: Props) {
  const [selectedLat, setSelectedLat] = useState(initialLocation.latitude);
  const [selectedLng, setSelectedLng] = useState(initialLocation.longitude);
  const [radius, setRadius] = useState(50);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleMapClick = (lat: number, lng: number) => {
    setSelectedLat(lat);
    setSelectedLng(lng);
  };

  const handleSave = async () => {
    setIsSaving(true);
    setError(null);
    try {
      const success = await createSafeArea(
        radius,
        selectedLat,
        selectedLng,
        animalId
      );
      if (success) {
        onClose(true); // Return to previous screen and reload
      } else {
        setError("Erro ao salvar área segura");
      }
    } catch (e: any) {
      setError(e.message || "Erro ao salvar área segura");
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-[var(--color-sand-100)] z-[100] flex flex-col">
      {/* Header */}
      <div className="bg-[var(--color-primary)] text-white p-4 flex items-center gap-4 shadow-md z-10 relative">
        <button onClick={() => onClose(false)} className="text-white text-xl">
          <FaArrowLeft />
        </button>
        <h1 className="text-lg font-semibold">Definir Área Segura</h1>
      </div>

      {/* Map Area */}
      <div className="flex-1 relative">
        <MapView
          lat={selectedLat}
          lng={selectedLng}
          hideMarker={true} // Ocultar o pino do animal
          onMapClick={handleMapClick}
          safeArea={{
            lat: selectedLat,
            lng: selectedLng,
            radius: radius,
          }}
        />

        {/* Instrução topo */}
        <div className="absolute top-4 left-4 right-4 bg-[var(--color-sand-100)]/90 backdrop-blur rounded-xl p-3 shadow-lg flex items-center gap-3">
          <FaInfoCircle className="text-orange-500 text-xl flex-shrink-0" />
          <p className="text-sm text-gray-700 font-medium">
            Toque no mapa para mover o centro da área
          </p>
        </div>

        {error && (
          <div className="absolute top-20 left-4 right-4 bg-red-100 text-red-700 p-3 rounded-lg shadow-lg">
            {error}
          </div>
        )}
      </div>

      {/* Painel Inferior */}
      <div className="bg-[var(--color-sand-100)] rounded-t-3xl shadow-[0_-4px_10px_rgba(0,0,0,0.1)] p-6 z-10 relative">
        <h2 className="text-lg font-bold text-gray-800">
          Configurar Área Segura
        </h2>
        
        <div className="mt-6">
          <div className="flex justify-between items-center mb-2">
            <span className="text-gray-600 font-medium">Raio:</span>
            <span className="text-orange-500 font-bold">{radius}m</span>
          </div>
          <input
            type="range"
            min="5"
            max="500"
            value={radius}
            onChange={(e) => setRadius(Number(e.target.value))}
            className="w-full accent-orange-500 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
          />
        </div>

        <button
          onClick={handleSave}
          disabled={isSaving}
          className="w-full mt-8 bg-[var(--color-primary)] disabled:bg-gray-400 text-white font-bold py-3 px-4 rounded-xl shadow-md hover:brightness-95 transition-all flex items-center justify-center"
        >
          {isSaving ? "Salvando..." : "Salvar Área Segura"}
        </button>
      </div>
    </div>
  );
}
