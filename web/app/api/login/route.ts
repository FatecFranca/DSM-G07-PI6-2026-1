import { NextResponse } from "next/server";

const JAVA_API = process.env.JAVA_API_URL;

export async function POST(req: Request) {
  try {
    const body = await req.json();

    const res = await fetch(`${JAVA_API}/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    const data = await res.json();

    return NextResponse.json(data, { status: res.status });
  } catch {
    return NextResponse.json({ error: "Erro no login" }, { status: 500 });
  }
}