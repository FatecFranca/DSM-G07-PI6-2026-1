"use client";

import { GoogleMap, useLoadScript, Marker } from "@react-google-maps/api";
import { useEffect } from "react";

const containerStyle = {
  width: "100%",
  height: "100%",
};

interface Props {
  lat: number;
  lng: number;
  onMapLoaded?: () => void;
  onError?: (err: string) => void;
}

export default function MapView({
  lat,
  lng,
  onMapLoaded,
  onError,
}: Props) {
  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY!,
  });

  // 🔥 trata erro real da API
  useEffect(() => {
    if (loadError && onError) {
      onError("Erro ao carregar Google Maps");
    }
  }, [loadError]);

  // 🔥 avisa quando mapa carregou
  useEffect(() => {
    if (isLoaded && onMapLoaded) {
      onMapLoaded();
    }
  }, [isLoaded]);

  // ❌ NÃO renderiza loading aqui (overlay cuida disso)
  if (!isLoaded) return null;

  return (
    <GoogleMap
      mapContainerStyle={containerStyle}
      center={{ lat, lng }}
      zoom={16}
      options={{
        disableDefaultUI: true,
      }}
    >
      <Marker position={{ lat, lng }} />
    </GoogleMap>
  );
}