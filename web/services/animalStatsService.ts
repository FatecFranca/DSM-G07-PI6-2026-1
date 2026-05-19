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
        `${PYTHON_API}/batimentos/animal/${animalId}/media-ultimos-5-dias`,
        { headers: this.getHeaders() }
      );
      if (!res.ok) throw new Error("Falha ao buscar médias dos últimos 5 dias");
      
      const data = await res.json();
      // O formato retornado pela API deve ser um dicionário { "YYYY-MM-DD": media } ou uma lista
      // Vamos tentar adaptar. Se for um dicionário de datas:
      if (typeof data === "object" && !Array.isArray(data)) {
        return Object.entries(data).map(([date, bpm]) => {
          // Format date from YYYY-MM-DD to DD/MM
          const [, month, day] = date.split("-");
          return {
            data: `${day}/${month}`,
            bpm: Math.round(Number(bpm)),
          };
        }).reverse(); // Ensure chronological order if necessary, but usually API handles it.
      }
      
      // Se for uma lista
      if (Array.isArray(data)) {
         return data.map((item: any) => {
           const dateStr = item.data || item.date;
           let formattedDate = dateStr;
           if (dateStr && typeof dateStr === "string" && dateStr.includes("-")) {
             const baseDate = dateStr.split("T")[0].split(" ")[0]; // "2025-10-17"
             const parts = baseDate.split("-");
             if (parts.length >= 3) {
               formattedDate = `${parts[2]}/${parts[1]}`;
             }
           }
           return {
             data: formattedDate,
             bpm: Math.round(item.media || item.bpm || item.valor),
           };
         });
      }

      return [];
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
        `${PYTHON_API}/batimentos/animal/${animalId}/media-ultimas-5-horas-registradas`,
        { headers: this.getHeaders() }
      );
      if (!res.ok) throw new Error("Falha ao buscar médias das últimas 5 horas");
      
      const data = await res.json();
      
      // Se for um dicionário de timestamps: { "2025-10-17 20:00:00-03:00": bpm }
      if (typeof data === "object" && !Array.isArray(data)) {
        return Object.entries(data).map(([date, bpm]) => {
          return {
            data: date, // Keep original timestamp so the chart can format it
            bpm: Math.round(Number(bpm)),
          };
        }).reverse();
      }
      
      // Se for uma lista de objetos
      if (Array.isArray(data)) {
         return data.map((item: any) => {
           return {
             data: item.data || item.date || item.timestamp || "",
             bpm: Math.round(item.media || item.bpm || item.valor || item.frequenciaMedia || 0),
           };
         });
      }

      return [];
    } catch (e) {
      console.error("[AnimalStatsService] getMediaUltimas5HorasRegistradas", e);
      return [];
    }
  }
}

export const animalStatsService = new AnimalStatsService();
