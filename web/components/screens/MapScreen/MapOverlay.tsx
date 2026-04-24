"use client";

export default function MapOverlay() {
  return (
    <>
      {/* loading */}
      <div className="absolute inset-0 bg-black/30 flex items-center justify-center">
        <span className="text-white">Loading...</span>
      </div>

      {/* erro */}
      <div className="absolute top-24 left-4 right-4 bg-red-100 p-4 rounded">
        Erro ao carregar localização
      </div>

      {/* alerta área segura */}
      <div className="absolute top-16 left-4 right-4 bg-red-100 p-3 rounded-xl text-center">
        Pet fora da área segura
      </div>
    </>
  );
}