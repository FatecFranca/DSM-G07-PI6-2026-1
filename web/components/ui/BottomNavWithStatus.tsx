"use client";

import StatusBar from "./StatusBar";
import NavBar from "./NavBar";

interface Props {
  currentIndex: number;
  onChange: (index: number) => void;
  lastBpm?: number | null;
  isConnected?: boolean;
}

export default function BottomNavWithStatus({
  currentIndex,
  onChange,
  lastBpm,
  isConnected = false,
}: Props) {
  return (
    <>
      {/* 📱 MOBILE */}
      <div className="fixed bottom-0 left-0 w-full flex flex-col md:hidden z-50">
        <StatusBar
          isConnected={isConnected}
          animalName="Uno"
          lastBpm={lastBpm ?? undefined}
        />

        <NavBar
          currentIndex={currentIndex}
          onChange={onChange}
        />
      </div>

      {/* 💻 DESKTOP */}
      <div className="hidden md:block">
        <div className="fixed bottom-[85px] left-0 w-[280px] z-40">
          <StatusBar
            isConnected={isConnected}
            animalName="Uno"
            lastBpm={lastBpm ?? undefined}
          />
        </div>

        <div className="fixed bottom-0 left-0 w-full z-50">
          <NavBar
            currentIndex={currentIndex}
            onChange={onChange}
          />
        </div>
      </div>
    </>
  );
}