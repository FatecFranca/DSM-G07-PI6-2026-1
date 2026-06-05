import { NextRequest, NextResponse } from "next/server";

const JAVA_API = process.env.JAVA_API_URL!;

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const animalId = searchParams.get("animalId");

  const token = req.headers.get("authorization");

  if (!animalId) {
    return NextResponse.json(
      { error: "animalId obrigatório" },
      { status: 400 }
    );
  }

  try {
    const [animalRes, heartbeatRes] = await Promise.all([
      fetch(`${JAVA_API}/animais/${animalId}`, {
        headers: {
          Authorization: token || "",
        },
        cache: "no-store",
      }),
      fetch(
        `${JAVA_API}/batimentos/animal/${animalId}/ultimo`,
        {
          headers: {
            Authorization: token || "",
          },
          cache: "no-store",
        }
      ),
    ]);

    if (!animalRes.ok) {
      return NextResponse.json(
        { error: "Erro ao buscar dados do animal" },
        { status: 500 }
      );
    }

    const animal = await animalRes.json();
    let bpm: number | null = null;

    if (heartbeatRes.ok) {
      try {
        const heartbeat = await heartbeatRes.json();
        bpm = heartbeat?.frequenciaMedia ?? null;
      } catch (err) {
        console.warn("Falha ao analisar JSON do ultimo batimento", err);
      }
    }

    return NextResponse.json({
      nome: animal.nome,
      sexo: animal.sexo,
      urlImagem: animal.urlImagem,
      bpm,
    });
  } catch (e) {
    return NextResponse.json(
      { error: "Erro interno" },
      { status: 500 }
    );
  }
}