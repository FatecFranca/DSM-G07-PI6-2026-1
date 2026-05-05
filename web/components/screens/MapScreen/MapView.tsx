"use client";

import { GoogleMap, useLoadScript } from "@react-google-maps/api";
import { useRef, useEffect } from "react";

const containerStyle = {
  width: "100%",
  height: "100%",
};

const libraries: ("marker")[] = ["marker"];

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
  const mapRef = useRef<google.maps.Map | null>(null);
  const markerRef = useRef<google.maps.marker.AdvancedMarkerElement | null>(null);

  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY!,
    libraries,
  });

  useEffect(() => {
    if (loadError && onError) {
      onError("Erro ao carregar Google Maps");
    }
  }, [loadError]);

  function createMarker(map: google.maps.Map) {
    const pin = document.createElement("div");

    pin.style.width = "62px";
    pin.style.height = "62px";
    pin.style.borderRadius = "50%";
    pin.style.overflow = "hidden";
    pin.style.border = "3px solid var(--color-orange-400)";
    pin.style.background = "var(--color-sand-100)"; 
    pin.style.boxShadow = "0 4px 10px rgba(0,0,0,0.3)";
    pin.style.display = "flex";
    pin.style.alignItems = "center";
    pin.style.justifyContent = "center";

    const img = document.createElement("img");
    img.src = "/images/uno.png";
    img.style.width = "100%";
    img.style.height = "100%";
    img.style.objectFit = "cover";

    pin.appendChild(img);

    markerRef.current = new google.maps.marker.AdvancedMarkerElement({
      map,
      position: { lat, lng },
      content: pin,
    });
  }

  useEffect(() => {
    if (markerRef.current) {
      markerRef.current.position = { lat, lng };
    }
  }, [lat, lng]);

  if (!isLoaded) return null;

  return (
    <GoogleMap
      mapContainerStyle={containerStyle}
      center={{ lat, lng }}
      zoom={16}
      options={{
        disableDefaultUI: true,
        mapId: "DEMO_MAP_ID",
      }}
      onLoad={(map) => {
        mapRef.current = map;
        createMarker(map);
        if (onMapLoaded) onMapLoaded();
      }}
    />
  );
}