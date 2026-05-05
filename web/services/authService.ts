"use client";

interface AuthResponse {
  token: string;
  userId: string;
  animalId: string;
  nome: string;
  email: string;
  petName: string;
}

class AuthService {
  private authData: AuthResponse | null = null;

  // 🔄 INIT + AUTO LOGIN
  async init() {
    try {
      const stored = localStorage.getItem("auth");

      if (stored) {
        this.authData = JSON.parse(stored);
        console.log("[AuthService] carregado do storage");
        return;
      }

      console.log("[AuthService] fazendo auto login...");

      const success = await this.login(
        "henriquealmeidaflorentino@gmail.com",
        "senha123"
      );

      if (!success) {
        console.error("[AuthService] falha no auto login");
      }
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

  isAuthenticated() {
    return !!this.getToken();
  }

  logout() {
    this.authData = null;
    localStorage.removeItem("auth");
  }
}

export const authService = new AuthService();