"use client";

import { authService } from "./authService";

// Usa o proxy local Next.js (/api) para contornar problemas de CORS no navegador
const PYTHON_API = "/api";


export interface HeartbeatData {
  data: string; // "YYYY-MM-DD" or formatted "DD/MM"
  bpm: number;
}

export interface AnaliseBatimento {
  batimentoAnalisado: number;
  titulo: string;
  interpretacao: string;
}

export class AnimalStatsService {
  private getHeaders() {
    const token = authService.getToken();
    if (!token) throw new Error("Usuário não autenticado");
    return {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    };
  }

  // 1. Média dos últimos 5 dias
  async getMediaUltimos5Dias(animalId: string): Promise<HeartbeatData[]> {
    try {
      const res = await fetch(
        `/api/batimentos/animal/${animalId}/media-ultimos-5-dias`,
        { headers: this.getHeaders() }
      );
      if (!res.ok) throw new Error("Falha ao buscar médias dos últimos 5 dias");
      
      const data = await res.json();
      const medias = data.medias || {};

      const list: HeartbeatData[] = Object.entries(medias).map(([dateStr, bpmValue]) => {
        return {
          data: dateStr,
          bpm: Math.round(Number(bpmValue)),
        };
      }).sort((a, b) => a.data.localeCompare(b.data));

      return list.slice(-5);
    } catch (e) {
      console.error("[AnimalStatsService] getMediaUltimos5Dias", e);
      return [];
    }
  }

  // 2. Média por data específica
  async getMediaPorData(animalId: string, date: string): Promise<number | null> {
    try {
      // date = YYYY-MM-DD
      const res = await fetch(
        `${PYTHON_API}/batimentos/animal/${animalId}/batimentos/media-por-data?inicio=${date}&fim=${date}`,
        { headers: this.getHeaders() }
      );
      if (!res.ok) throw new Error("Falha ao buscar média por data");
      
      const data = await res.json();
      // data: { "media": 79.5 } ou algo similar
      if (data && data.media !== undefined && data.media !== null) {
        return Math.round(data.media);
      }
      return null;
    } catch (e) {
      console.error("[AnimalStatsService] getMediaPorData", e);
      return null;
    }
  }

  // 3. Análise do último batimento
  async getAnaliseUltimoBatimento(animalId: string): Promise<AnaliseBatimento | null> {
    try {
      const res = await fetch(
        `${PYTHON_API}/batimentos/animal/${animalId}/ultimo/analise`,
        { headers: this.getHeaders() }
      );
      if (!res.ok) throw new Error("Falha ao buscar análise");

      const data = await res.json();
      // Retorno esperado da API baseado no Flutter: titulo, interpretacao, batimentoAnalisado
      return {
        batimentoAnalisado: Math.round(data.batimentoAnalisado || data.batimento || data.valor || 0),
        titulo: data.titulo || "Batimento Normal",
        interpretacao: data.interpretacao || "O batimento está dentro dos padrões normais.",
      };
    } catch (e) {
      console.error("[AnimalStatsService] getAnaliseUltimoBatimento", e);
      return null;
    }
  }

  // 4. Média das últimas 5 horas registradas
  async getMediaUltimas5HorasRegistradas(animalId: string): Promise<HeartbeatData[]> {
    try {
      const res = await fetch(
        `/api/batimentos/animal/${animalId}/media-ultimas-5-horas-registradas`,
        { headers: this.getHeaders() }
      );
      if (!res.ok) throw new Error("Falha ao buscar médias das últimas 5 horas");
      
      const data = await res.json();
      const mediaPorHora = data.media_por_hora || {};

      const list: HeartbeatData[] = Object.entries(mediaPorHora).map(([hourStr, bpmValue]) => {
        return {
          data: hourStr,
          bpm: Math.round(Number(bpmValue)),
        };
      }).sort((a, b) => a.data.localeCompare(b.data));

      return list.slice(-5);
    } catch (e) {
      console.error("[AnimalStatsService] getMediaUltimas5HorasRegistradas", e);
      return [];
    }
  }
}

export const animalStatsService = new AnimalStatsService();
