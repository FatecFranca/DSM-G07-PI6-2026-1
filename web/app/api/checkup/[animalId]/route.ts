import { NextRequest, NextResponse } from "next/server";

const PYTHON_API = process.env.NEXT_PUBLIC_API_PYTHON_URL || "http://34.24.9.134:8083";

export async function POST(
  req: NextRequest,
  { params }: { params: Promise<{ animalId: string }> }
) {
  try {
    const { animalId } = await params;

    if (!animalId) {
      return NextResponse.json(
        { error: "animalId obrigatório" },
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

    // Obter o corpo do JSON enviado pelo frontend
    const body = await req.json();

    const targetUrl = `${PYTHON_API}/ia/checkup/animal/${animalId}`;
    console.log(`[Proxy Checkup] Redirecionando POST para ${targetUrl}`);

    const res = await fetch(targetUrl, {
      method: "POST",
      headers: {
        Authorization: authHeader,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
      cache: "no-store",
    });

    if (!res.ok) {
      const text = await res.text();
      console.error(`[Proxy Checkup] Erro ${res.status}: ${text}`);
      return NextResponse.json(
        {
          error: "Erro ao enviar respostas para a API Python",
          details: text,
        },
        { status: res.status }
      );
    }

    const data = await res.json();
    console.log(`[Proxy Checkup] Resposta recebida da API Python:`, data);
    return NextResponse.json(data);
  } catch (e) {
    console.error("[Proxy Checkup] Erro interno:", e);
    return NextResponse.json(
      { error: "Erro interno no proxy de checkup" },
      { status: 500 }
    );
  }
}
