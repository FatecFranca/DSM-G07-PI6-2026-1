import { NextRequest, NextResponse } from "next/server";

const PYTHON_API = process.env.NEXT_PUBLIC_API_PYTHON_URL || "http://34.24.9.134:8083";

export async function GET(req: NextRequest) {
  try {
    const urlObj = new URL(req.url);
    const pathname = urlObj.pathname;
    const search = urlObj.search;

    // Subtitui o prefixo local "/api/batimentos" por "/batimentos" para montar a rota da API Python
    const targetPath = pathname.replace(/^\/api\/batimentos/, "/batimentos");
    const targetUrl = `${PYTHON_API}${targetPath}${search}`;

    console.log(`[Proxy batimentos] Redirecionando ${pathname} -> ${targetUrl}`);

    const authHeader = req.headers.get("authorization");
    if (!authHeader) {
      return NextResponse.json(
        { error: "Token não enviado" },
        { status: 401 }
      );
    }

    const res = await fetch(targetUrl, {
      headers: {
        Authorization: authHeader,
        "Content-Type": "application/json",
      },
      cache: "no-store",
    });

    if (!res.ok) {
      const text = await res.text();
      console.error(`[Proxy batimentos] Erro ${res.status}: ${text}`);
      return NextResponse.json(
        {
          error: "Erro ao buscar dados da API Python",
          details: text,
        },
        { status: res.status }
      );
    }

    const data = await res.json();
    return NextResponse.json(data);
  } catch (e) {
    console.error("[Proxy batimentos] Erro interno:", e);
    return NextResponse.json(
      { error: "Erro interno no proxy de batimentos" },
      { status: 500 }
    );
  }
}
