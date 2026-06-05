"use client";

interface AuthResponse {
  token: string;
  userId: string;
  animalId: string;
  nome: string;
  email: string;
  petName: string;
  animalImagemUrl?: string;
}

class AuthService {
  private authData: AuthResponse | null = null;

  // 🔄 INIT
  async init() {
    try {
      const stored = localStorage.getItem("auth");

      if (stored) {
        this.authData = JSON.parse(stored);
        console.log("[AuthService] carregado do storage");
        return;
      }
      console.log("[AuthService] nenhuma credencial salva encontrada.");
    } catch (e) {
      console.error("[AuthService] erro init:", e);
    }
  }

  // 🔐 LOGIN (via proxy)
  async login(email: string, senha: string): Promise<boolean> {
    try {
      const res = await fetch("/api/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, senha }),
      });

      if (!res.ok) {
        const data = await res.json();
        console.error("[AuthService] erro login:", data);
        return false;
      }

      const data: AuthResponse = await res.json();

      this.authData = data;
      localStorage.setItem("auth", JSON.stringify(data));

      console.log("[AuthService] login sucesso");

      return true;
    } catch (e) {
      console.error("[AuthService] erro login:", e);
      return false;
    }
  }

  getToken() {
    return this.authData?.token;
  }

  getAnimalId() {
    return this.authData?.animalId;
  }

  getUserId() {
    return this.authData?.userId;
  }

  getNome() {
    return this.authData?.nome;
  }

  getEmail() {
    return this.authData?.email;
  }

  getPetName() {
    return this.authData?.petName;
  }

  getAnimalImagemUrl() {
    return this.authData?.animalImagemUrl;
  }

  isAuthenticated() {
    return !!this.getToken();
  }

  logout() {
    this.authData = null;
    localStorage.removeItem("auth");
  }
}

export const authService = new AuthService();