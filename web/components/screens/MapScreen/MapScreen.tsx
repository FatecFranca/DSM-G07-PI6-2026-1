"use client";

import MapView from "./MapView";
import MapOverlay from "./MapOverlay";
import MapActions from "./MapActions";

export default function MapScreen() {
  return (
    <div className="relative w-full h-screen">
      <MapView />

      <MapOverlay />

      <MapActions />
    </div>
  );
}