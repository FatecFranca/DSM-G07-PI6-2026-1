import { NextRequest, NextResponse } from "next/server";

const BASE = "http://34.24.9.134:8080";

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const animalId = searchParams.get("animalId");

  const token = req.headers.get("authorization");

  if (!animalId) {
    return NextResponse.json({ error: "animalId obrigatório" }, { status: 400 });
  }

  try {
    const [animalRes, heartbeatRes] = await Promise.all([
      fetch(`${BASE}/animais/${animalId}`, {
        headers: { Authorization: token || "" },
      }),
      fetch(`${BASE}/batimentos/animal/${animalId}/ultimo`, {
        headers: { Authorization: token || "" },
      }),
    ]);

    if (!animalRes.ok || !heartbeatRes.ok) {
      return NextResponse.json({ error: "Erro ao buscar dados" }, { status: 500 });
    }

    const animal = await animalRes.json();
    const heartbeat = await heartbeatRes.json();

    return NextResponse.json({
      nome: animal.nome,
      sexo: animal.sexo,
      bpm: heartbeat.frequenciaMedia,
    });
  } catch (e) {
    return NextResponse.json({ error: "Erro interno" }, { status: 500 });
  }
}