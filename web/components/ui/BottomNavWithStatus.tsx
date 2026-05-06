"use client";

import StatusBar from "./StatusBar";
import NavBar from "./NavBar";

interface Props {
  currentIndex: number;
  onChange: (index: number) => void;
}

export default function BottomNavWithStatus({
  currentIndex,
  onChange,
}: Props) {
  return (
    <>
      {/* 📱 MOBILE (PERFEITO - mantém igual) */}
      <div className="fixed bottom-0 left-0 w-full flex flex-col md:hidden z-50">
        <StatusBar isConnected={true} animalName="Uno" />
        <NavBar currentIndex={currentIndex} onChange={onChange} />
      </div>

      {/* 💻 DESKTOP (CORRIGIDO) */}
      <div className="hidden md:block">
        
        {/* STATUS BAR lateral, MAS grudada embaixo */}
        <div className="fixed bottom-[85px] left-0 w-[280px] z-40">
          <StatusBar isConnected={true} animalName="Uno" />
        </div>

        {/* NAVBAR embaixo */}
        <div className="fixed bottom-0 left-0 w-full z-50">
          <NavBar currentIndex={currentIndex} onChange={onChange} />
        </div>
      </div>
    </>
  );
}