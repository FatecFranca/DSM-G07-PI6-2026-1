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
  safeArea?: {
    lat: number;
    lng: number;
    radius: number;
  } | null;
  onMapClick?: (lat: number, lng: number) => void;
  hideMarker?: boolean;
}

export default function MapView({
  lat,
  lng,
  onMapLoaded,
  onError,
  safeArea,
  onMapClick,
  hideMarker = false,
}: Props) {
  const mapRef = useRef<google.maps.Map | null>(null);
  const markerRef = useRef<google.maps.marker.AdvancedMarkerElement | null>(null);
  const circleRef = useRef<google.maps.Circle | null>(null);

  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY?.trim() || "",
    libraries,
  });

  useEffect(() => {
    if (loadError && onError) {
      onError("Erro ao carregar Google Maps");
    }
  }, [loadError]);

  function createMarker(map: google.maps.Map) {
    if (hideMarker) return;
    if (markerRef.current) return;

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
    if (mapRef.current) {
      mapRef.current.panTo({ lat, lng });
    }
  }, [lat, lng]);

  useEffect(() => {
    if (!mapRef.current) return;

    if (safeArea) {
      if (!circleRef.current) {
        circleRef.current = new google.maps.Circle({
          map: mapRef.current,
          center: { lat: safeArea.lat, lng: safeArea.lng },
          radius: safeArea.radius,
          fillColor: "rgba(25, 118, 210, 0.2)",
          strokeColor: "#1976D2",
          strokeWeight: 2,
        });
      } else {
        circleRef.current.setCenter({ lat: safeArea.lat, lng: safeArea.lng });
        circleRef.current.setRadius(safeArea.radius);
      }
    } else {
      if (circleRef.current) {
        circleRef.current.setMap(null);
        circleRef.current = null;
      }
    }
  }, [safeArea, isLoaded]); // Depends on safeArea and isLoaded

  // Cleanup map resources on unmount
  useEffect(() => {
    return () => {
      if (circleRef.current) {
        circleRef.current.setMap(null);
        circleRef.current = null;
      }
      if (markerRef.current) {
        markerRef.current.map = null;
        markerRef.current = null;
      }
    };
  }, []);

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
      onClick={(e) => {
        if (onMapClick && e.latLng) {
          onMapClick(e.latLng.lat(), e.latLng.lng());
        }
      }}
      onLoad={(map) => {
        mapRef.current = map;
        createMarker(map);
        
        // Force initial circle render if safeArea already exists
        if (safeArea && !circleRef.current) {
          circleRef.current = new google.maps.Circle({
            map: map,
            center: { lat: safeArea.lat, lng: safeArea.lng },
            radius: safeArea.radius,
            fillColor: "rgba(25, 118, 210, 0.2)",
            strokeColor: "#1976D2",
            strokeWeight: 2,
          });
        }
        
        if (onMapLoaded) onMapLoaded();
      }}
    />
  );
}