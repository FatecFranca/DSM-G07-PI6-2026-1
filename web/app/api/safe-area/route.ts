import { NextRequest, NextResponse } from "next/server";

const JAVA_API = process.env.JAVA_API_URL;

export async function POST(req: NextRequest) {
  try {
    const authHeader = req.headers.get("authorization");
    if (!authHeader) {
      return NextResponse.json({ error: "Token não enviado" }, { status: 401 });
    }

    const body = await req.json();

    const url = `${JAVA_API}/areas-seguras`;

    const res = await fetch(url, {
      method: "POST",
      headers: {
        Authorization: authHeader,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    if (!res.ok) {
      const text = await res.text();
      return NextResponse.json(
        { error: "Erro ao criar área segura", details: text },
        { status: res.status }
      );
    }

    // Algumas APIs retornam 201 Created vazio, então verificamos
    const text = await res.text();
    const data = text ? JSON.parse(text) : { success: true };

    return NextResponse.json(data, { status: res.status });
  } catch (e) {
    console.error("Erro API route POST safe-area:", e);
    return NextResponse.json({ error: "Erro interno" }, { status: 500 });
  }
}

export async function GET(req: NextRequest) {
  try {
    const { searchParams } = new URL(req.url);
    const animalId = searchParams.get("animalId");

    if (!animalId) {
      return NextResponse.json(
        { error: "animalId é obrigatório" },
        { status: 400 }
      );
    }

    const authHeader = req.headers.get("authorization");
    if (!authHeader) {
      return NextResponse.json({ error: "Token não enviado" }, { status: 401 });
    }

    const url = `${JAVA_API}/areas-seguras/animal/${animalId}`;

    const res = await fetch(url, {
      headers: {
        Authorization: authHeader,
      },
      cache: "no-store",
    });

    if (res.status === 404) {
      return NextResponse.json({ error: "Área segura não encontrada" }, { status: 404 });
    }

    if (!res.ok) {
      const text = await res.text();
      return NextResponse.json(
        { error: "Erro ao buscar área segura", details: text },
        { status: res.status }
      );
    }

    const data = await res.json();
    return NextResponse.json(data);
  } catch (e) {
    console.error("Erro API route GET safe-area:", e);
    return NextResponse.json({ error: "Erro interno" }, { status: 500 });
  }
}
