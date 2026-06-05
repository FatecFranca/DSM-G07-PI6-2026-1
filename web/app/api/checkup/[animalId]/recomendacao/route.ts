import { NextRequest, NextResponse } from "next/server";

const PYTHON_API = process.env.NEXT_PUBLIC_API_PYTHON_URL || "http://34.24.9.134:8083";

export async function GET(
  req: NextRequest,
  { params }: { params: Promise<{ animalId: string }> }
) {
  try {
    const { animalId } = await params;
    const { searchParams } = new URL(req.url);
    const pesoIdeal = searchParams.get("pesoIdeal");

    if (!animalId) {
      return NextResponse.json(
        { error: "animalId obrigatório" },
        { status: 400 }
      );
    }

    if (!pesoIdeal) {
      return NextResponse.json(
        { error: "pesoIdeal obrigatório" },
        { status: 400 }
      );
    }

    const authHeader = req.headers.get("authorization");
    if (!authHeader) {
      return NextResponse.json(
        { error: "Token não enviado" },
        { status: 401 }
      );
    }

    const targetUrl = `${PYTHON_API}/animal/${animalId}/ia-recomendacao?pesoIdeal=${pesoIdeal}`;
    console.log(`[Proxy Recomendação Ração] GET ${targetUrl}`);

    const res = await fetch(targetUrl, {
      method: "GET",
      headers: {
        Authorization: authHeader,
        "Content-Type": "application/json",
      },
      cache: "no-store",
    });

    if (!res.ok) {
      const text = await res.text();
      console.error(`[Proxy Recomendação Ração] Erro ${res.status}: ${text}`);
      return NextResponse.json(
        {
          error: "Erro ao buscar recomendação de ração na API Python",
          details: text,
        },
        { status: res.status }
      );
    }

    const data = await res.json();
    console.log(`[Proxy Recomendação Ração] Resposta recebida da API Python:`, data);
    return NextResponse.json(data);
  } catch (e) {
    console.error("[Proxy Recomendação Ração] Erro interno:", e);
    return NextResponse.json(
      { error: "Erro interno no proxy de recomendação de ração" },
      { status: 500 }
    );
  }
}
