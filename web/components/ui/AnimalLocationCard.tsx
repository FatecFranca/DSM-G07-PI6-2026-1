"use client";

import { useEffect, useState } from "react";
import MapView from "@/components/screens/MapScreen/MapView";
import {
  getUltimaLocalizacaoAnimal,
  getEnderecoFromCoordinates,
} from "@/services/locationService";

interface Props {
  animalId: string;
  animalName: string;
}

export default function AnimalLocationCard({
  animalId,
  animalName,
}: Props) {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [lat, setLat] = useState<number | null>(null);
  const [lng, setLng] = useState<number | null>(null);
  const [address, setAddress] = useState<string | null>(null);

  async function loadLocation() {
    try {
      setLoading(true);
      setError(null);

      const location = await getUltimaLocalizacaoAnimal(animalId);

      if (!location) {
        setError(`Nenhuma localização encontrada para ${animalName}`);
        return;
      }

      setLat(location.latitude);
      setLng(location.longitude);

      const addr = await getEnderecoFromCoordinates(
        location.latitude,
        location.longitude
      );

      setAddress(addr);
    } catch (err) {
      setError("Erro ao carregar localização");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadLocation();
  }, []);

  return (
    <div className="m-4 p-5 bg-white rounded-xl shadow-md">
      {/* HEADER */}
      <div className="flex items-center gap-2 mb-4">
        <span className="text-orange-500 text-xl">📍</span>
        <h2 className="font-semibold text-lg">
          Localização de {animalName}
        </h2>
      </div>

      {/* LOADING */}
      {loading && (
        <div className="flex justify-center py-10">
          <div className="animate-spin w-6 h-6 border-2 border-orange-500 border-t-transparent rounded-full" />
        </div>
      )}

      {/* ERRO */}
      {error && (
        <div className="bg-red-100 border border-red-300 p-3 rounded text-sm text-red-700">
          {error}
        </div>
      )}

      {/* MAPA */}
      {!loading && !error && lat && lng && (
        <>
          <div className="h-[250px] rounded-lg overflow-hidden">
            <MapView lat={lat} lng={lng} />
          </div>

          {/* ENDEREÇO */}
          {address && (
            <div className="mt-4 p-3 bg-[var(--color-sand-100)] rounded">
              📍 {address}
            </div>
          )}
        </>
      )}

      {/* BOTÃO */}
      <button
        onClick={loadLocation}
        className="mt-4 w-full bg-[#F57C00] text-white py-2 rounded font-semibold hover:opacity-90"
      >
        Atualizar Localização
      </button>
    </div>
  );
}