export async function getEnderecoAtualDoAnimal(lat: number, lng: number) {
  try {
    const apiKey = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY?.trim();

    if (!apiKey) return null;

    const res = await fetch(
      `https://maps.googleapis.com/maps/api/geocode/json?latlng=${lat},${lng}&key=${apiKey}&language=pt-BR`
    );

    const data = await res.json();
    console.log("📍 API Geocoding:", data);

    if (data.status === "OK" && data.results.length > 0) {
      return data.results[0].formatted_address;
    }

    return null;
  } catch {
    return null;
  }
}