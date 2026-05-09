"use client";

import { authService } from "./authService";

export interface SafeArea {
  id?: string;
  raio: number;
  latitude: number;
  longitude: number;
  animal: string;
}

export async function createSafeArea(
  raio: number,
  latitude: number,
  longitude: number,
  animalId: string
): Promise<boolean> {
  try {
    const token = authService.getToken();
    if (!token) throw new Error("Usuário não autenticado");

    const body = {
      raio,
      latitude,
      longitude,
      animal: animalId,
    };

    const res = await fetch("/api/safe-area", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    if (!res.ok) {
      throw new Error("Erro ao criar área segura");
    }

    return true;
  } catch (error) {
    console.error("Erro no safeAreaService.createSafeArea:", error);
    return false;
  }
}

export async function getSafeAreaByAnimalId(
  animalId: string
): Promise<SafeArea | null> {
  try {
    const token = authService.getToken();
    if (!token) throw new Error("Usuário não autenticado");

    const res = await fetch(`/api/safe-area?animalId=${animalId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (res.status === 404) {
      return null;
    }

    if (!res.ok) {
      throw new Error("Erro ao buscar área segura");
    }

    const data = await res.json();
    return data;
  } catch (error) {
    console.error("Erro no safeAreaService.getSafeAreaByAnimalId:", error);
    return null;
  }
}
