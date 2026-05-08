import { NextResponse } from "next/server";

const JAVA_API = process.env.JAVA_API_URL;

export async function GET(req: Request) {
  try {
    const { searchParams } = new URL(req.url);
    const animalId = searchParams.get("animalId");

    if (!animalId) {
      return NextResponse.json(
        { error: "animalId é obrigatório" },
        { status: 400 }
      );
    }

    // 🔥 PEGA O TOKEN DO HEADER
    const authHeader = req.headers.get("authorization");

    if (!authHeader) {
      return NextResponse.json(
        { error: "Token não enviado" },
        { status: 401 }
      );
    }

    const url = `${JAVA_API}/localizacoes/animal/${animalId}/ultima`;

    // 🔥 REPASSA O TOKEN PRA API JAVA
    const res = await fetch(url, {
      headers: {
        Authorization: authHeader,
      },
      cache: "no-store",
    });

    if (!res.ok) {
      const text = await res.text();

      return NextResponse.json(
        {
          error: "Erro ao buscar localização",
          details: text,
        },
        { status: res.status }
      );
    }

    const data = await res.json();

    return NextResponse.json(data);
  } catch (e) {
    console.error("Erro API route:", e);

    return NextResponse.json(
      { error: "Erro interno" },
      { status: 500 }
    );
  }
}