"use client";

import { authService } from "./authService";

export interface AnimalData {
  nome: string;
  sexo: "M" | "F";
  bpm: number;
}

export async function getAnimalData(
  animalId: string
): Promise<AnimalData | null> {
  try {
    const token = authService.getToken();

    if (!token) {
      throw new Error("Usuário não autenticado");
    }

    console.log("🔍 Buscando dados do animal...");

    const res = await fetch(`/api/animal?animalId=${animalId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!res.ok) {
      const data = await res.json();
      throw new Error(data.error || "Erro ao buscar animal");
    }

    const data = await res.json();

    console.log("✅ Animal carregado:", data);
    console.log("❤️ BPM recebido:", data.bpm);

    return data;
  } catch (error) {
    console.error("❌ Erro animalService:", error);
    return null;
  }
}