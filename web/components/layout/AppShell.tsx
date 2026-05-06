"use client";

import { useState } from "react";
import MapScreen from "@/components/screens/MapScreen/MapScreen";
import BottomNavWithStatus from "@/components/ui/BottomNavWithStatus";

export default function AppShell() {
  const [currentIndex, setCurrentIndex] = useState(0);

  const pages = [
    <MapScreen key="map" />,
    <div key="health">Health</div>,
    <div key="checkup">Checkup</div>,
    <div key="location">Location</div>,
  ];

  return (
    <div className="h-screen overflow-hidden">
      {pages[currentIndex]}

      <BottomNavWithStatus
        currentIndex={currentIndex}
        onChange={setCurrentIndex}
      />
    </div>
  );
}