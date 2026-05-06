"use client";

interface Props {
  isLoaded: boolean;
  isLoadingLocation: boolean;
  error: string | null;
  isOutsideSafeZone: boolean;
}

export default function MapOverlay({
  isLoaded,
  isLoadingLocation,
  error,
  isOutsideSafeZone,
}: Props) {
  return (
    <>
      {/* LOADING */}
      {(!isLoaded || isLoadingLocation) && (
        <div className="absolute inset-0 bg-black/30 flex items-center justify-center z-50">
          <span className="text-white">Carregando mapa...</span>
        </div>
      )}

      {/* ERRO */}
      {error && (
        <div className="absolute top-24 left-4 right-4 bg-red-100 p-4 rounded z-50">
          {error}
        </div>
      )}

      {/* ALERTA */}
      {isOutsideSafeZone && (
        <div className="absolute top-16 left-4 right-4 bg-red-100 p-3 rounded-xl text-center z-50">
          Pet fora da área segura
        </div>
      )}
    </>
  );
}