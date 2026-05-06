"use client";

import { authService } from "./authService";

export interface LocationData {
  latitude: number;
  longitude: number;
}

export async function getUltimaLocalizacaoAnimal(
  animalId: string
): Promise<LocationData | null> {
  try {
    const token = authService.getToken();

    if (!token) {
      throw new Error("Usuário não autenticado");
    }

    const res = await fetch(`/api/location?animalId=${animalId}`, {
      headers: {
        Authorization: `Bearer ${token}`, // 🔥 ESSENCIAL
      },
    });

    if (!res.ok) {
      const data = await res.json();
      throw new Error(data.error || "Erro ao buscar localização");
    }

    const data = await res.json();

    return {
      latitude: data.latitude,
      longitude: data.longitude,
    };
  } catch (error) {
    console.error("Erro locationService:", error);
    return null;
  }
}