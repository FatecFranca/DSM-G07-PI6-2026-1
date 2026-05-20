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
        `/api/batimentos-history?animalId=${animalId}`,
        { headers: this.getHeaders() }
      );
      if (!res.ok) throw new Error("Falha ao buscar médias dos últimos 5 dias");
      
      const pageData = await res.json();
      const content = pageData.content || [];

      // Filtra registros com data futura (limite: final do dia 2026-05-20)
      const maxDate = new Date("2026-05-20T23:59:59-03:00").getTime();
      const validRecords = content.filter((item: any) => {
        if (!item.data) return false;
        const itemTime = new Date(item.data).getTime();
        return !isNaN(itemTime) && itemTime <= maxDate;
      });

      // Agrupa os registros por dia (YYYY-MM-DD)
      const groupedByDay: { [dateStr: string]: { sum: number; count: number } } = {};
      validRecords.forEach((item: any) => {
        const dateStr = item.data.split("T")[0]; // YYYY-MM-DD
        if (!groupedByDay[dateStr]) {
          groupedByDay[dateStr] = { sum: 0, count: 0 };
        }
        groupedByDay[dateStr].sum += item.frequenciaMedia || 0;
        groupedByDay[dateStr].count += 1;
      });

      // Calcula as médias, ordena cronologicamente e pega os últimos 5 dias
      const days = Object.entries(groupedByDay)
        .map(([dateStr, stats]) => {
          const [, month, day] = dateStr.split("-");
          return {
            dateStr,
            data: `${day}/${month}`,
            bpm: Math.round(stats.sum / stats.count),
          };
        })
        .sort((a, b) => a.dateStr.localeCompare(b.dateStr));

      return days.slice(-5);
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
        `/api/batimentos-history?animalId=${animalId}`,
        { headers: this.getHeaders() }
      );
      if (!res.ok) throw new Error("Falha ao buscar médias das últimas 5 horas");
      
      const pageData = await res.json();
      const content = pageData.content || [];

      // Filtra registros com data futura (limite: final do dia 2026-05-20)
      const maxDate = new Date("2026-05-20T23:59:59-03:00").getTime();
      const validRecords = content.filter((item: any) => {
        if (!item.data) return false;
        const itemTime = new Date(item.data).getTime();
        return !isNaN(itemTime) && itemTime <= maxDate;
      });

      // Agrupa por hora (YYYY-MM-DDTHH:00:00)
      const groupedByHour: { [hourStr: string]: { sum: number; count: number } } = {};
      validRecords.forEach((item: any) => {
        const d = new Date(item.data);
        const year = d.getFullYear();
        const month = String(d.getMonth() + 1).padStart(2, "0");
        const day = String(d.getDate()).padStart(2, "0");
        const hour = String(d.getHours()).padStart(2, "0");
        
        const hourStr = `${year}-${month}-${day}T${hour}:00:00`;
        if (!groupedByHour[hourStr]) {
          groupedByHour[hourStr] = { sum: 0, count: 0 };
        }
        groupedByHour[hourStr].sum += item.frequenciaMedia || 0;
        groupedByHour[hourStr].count += 1;
      });

      // Calcula as médias, ordena cronologicamente e pega as últimas 5 horas
      const hours = Object.entries(groupedByHour)
        .map(([hourStr, stats]) => {
          return {
            hourStr,
            data: hourStr,
            bpm: Math.round(stats.sum / stats.count),
          };
        })
        .sort((a, b) => a.hourStr.localeCompare(b.hourStr));

      return hours.slice(-5);
    } catch (e) {
      console.error("[AnimalStatsService] getMediaUltimas5HorasRegistradas", e);
      return [];
    }
  }
}

export const animalStatsService = new AnimalStatsService();
