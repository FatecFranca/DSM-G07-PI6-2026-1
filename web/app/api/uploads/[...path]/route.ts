import { NextRequest, NextResponse } from "next/server";

const JAVA_API = process.env.JAVA_API_URL!;

export async function GET(
  req: NextRequest,
  { params }: { params: Promise<{ path: string[] }> }
) {
  const token = req.headers.get("authorization");
  const { path } = await params;
  const imagePath = path.join("/");

  try {
    console.log(`[Proxy Image] Fetching from Java API: ${JAVA_API}/uploads/${imagePath}`);
    
    const res = await fetch(`${JAVA_API}/uploads/${imagePath}`, {
      headers: {
        Authorization: token || "",
      },
    });

    if (!res.ok) {
      const errorText = await res.text().catch(() => "");
      console.error(`[Proxy Image] Failed to fetch image: ${res.status} ${res.statusText}. Backend response: ${errorText}`);
      return new NextResponse(errorText || "Backend error", { status: res.status });
    }

    const contentType = res.headers.get("content-type") || "image/jpeg";
    const data = await res.arrayBuffer();

    return new NextResponse(data, {
      status: 200,
      headers: {
        "Content-Type": contentType,
        "Cache-Control": "public, max-age=31536000, immutable",
      },
    });
  } catch (err: any) {
    console.error("[Proxy Image] Error proxying image:", err);
    return new NextResponse(JSON.stringify({ 
      error: "Internal proxy error", 
      message: err.message, 
      stack: err.stack 
    }), { 
      status: 500,
      headers: {
        "Content-Type": "application/json"
      }
    });
  }
}
