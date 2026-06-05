import { authService } from "./authService";

export async function fetchAuthenticatedImage(url: string): Promise<string> {
  const token = authService.getToken();
  if (!token) {
    throw new Error("No auth token available");
  }

  // Rewrite /uploads/... to relative /api/uploads/... to call our Next.js API route proxy and avoid CORS
  let targetUrl = url;
  if (url.includes("/uploads/")) {
    const uploadsIndex = url.indexOf("/uploads/");
    targetUrl = "/api" + url.substring(uploadsIndex);
  }

  console.log(`[imageService] Fetching authenticated image via proxy: ${targetUrl}`);

  const res = await fetch(targetUrl, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!res.ok) {
    const errText = await res.text().catch(() => "");
    throw new Error(`Failed to fetch image: ${res.status} ${res.statusText}. Details: ${errText}`);
  }

  const blob = await res.blob();
  return URL.createObjectURL(blob);
}
