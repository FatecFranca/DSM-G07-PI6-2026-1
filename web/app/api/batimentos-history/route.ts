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
    const res = await fetch(
      `${JAVA_API}/batimentos/animal/${animalId}?size=200&sortBy=id&direction=desc`,
      {
        headers: {
          Authorization: token || "",
        },
        cache: "no-store",
      }
    );

    if (!res.ok) {
      return NextResponse.json(
        { error: "Erro ao buscar histórico de batimentos" },
        { status: res.status }
      );
    }

    const data = await res.json();
    return NextResponse.json(data);
  } catch (e) {
    console.error("[Proxy batimentos-history] Erro:", e);
    return NextResponse.json(
      { error: "Erro interno no proxy de histórico de batimentos" },
      { status: 500 }
    );
  }
}
