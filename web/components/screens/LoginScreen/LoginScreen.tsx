"use client";

import { useState } from "react";
import { FaEnvelope, FaLock, FaCheckCircle, FaMobileAlt } from "react-icons/fa";
import { authService } from "@/services/authService";
import Input from "@/components/ui/Input";

interface LoginScreenProps {
  onLoginSuccess: () => void;
}

export default function LoginScreen({ onLoginSuccess }: LoginScreenProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email.trim() || !password.trim()) {
      setErrorMessage("Por favor, preencha todos os campos.");
      return;
    }

    setIsLoading(true);
    setErrorMessage(null);

    try {
      console.log("[LoginScreen] Tentando realizar login para:", email.trim());
      const success = await authService.login(email.trim(), password.trim());

      if (success) {
        console.log("[LoginScreen] Login bem-sucedido!");
        onLoginSuccess();
      } else {
        setErrorMessage("E-mail ou senha inválidos. Tente novamente.");
      }
    } catch (err) {
      console.error(err);
      setErrorMessage("Ocorreu um erro ao tentar fazer login. Tente novamente.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleTestUserLogin = async () => {
    setIsLoading(true);
    setErrorMessage(null);
    try {
      console.log("[LoginScreen] Tentando realizar login com usuário teste...");
      const success = await authService.login("henriquealmeidaflorentino@gmail.com", "senha123");

      if (success) {
        console.log("[LoginScreen] Login de teste bem-sucedido!");
        onLoginSuccess();
      } else {
        setErrorMessage("Erro ao conectar com a conta de teste. Tente novamente.");
      }
    } catch (err) {
      console.error(err);
      setErrorMessage("Erro ao tentar fazer login com usuário teste.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="relative w-screen h-screen overflow-hidden bg-[var(--color-sand-100)] flex flex-col md:flex-row items-stretch font-sans">

      {/* 🐕 IMAGEM DE FUNDO (Watermark) - MOBILE */}
      <div
        className="absolute bottom-0 left-[-50px] right-0 h-[60vh] md:hidden bg-cover bg-center opacity-20 pointer-events-none"
        style={{
          backgroundImage: "url('/images/cao-dex.png')",
          backgroundRepeat: "no-repeat",
          backgroundPosition: "bottom left",
        }}
      />

      {/* 🐕 ESQUERDA (DESKTOP) - Large dog watermark blending into sand background */}
      <div className="hidden md:flex md:w-1/2 bg-[var(--color-sand-100)] relative overflow-hidden items-end justify-start">
        <div
          className="absolute left-[-30px] bottom-[-40px] w-[110%] h-[90%] bg-contain bg-left-bottom bg-no-repeat opacity-25 pointer-events-none"
          style={{
            backgroundImage: "url('/images/cao-dex.png')",
          }}
        />
      </div>

      {/* 🔒 CONTEÚDO PRINCIPAL (Direita no Desktop / Centralizado no Mobile) */}
      <div className="flex-1 flex items-center justify-center px-6 py-12 z-10 relative">
        <div className="w-full max-w-sm flex flex-col items-stretch md:-translate-x-24">

          {/* CABEÇALHO */}
          <h2 className="text-[var(--color-primary)] text-[24px] font-bold text-center mb-10 tracking-tight font-poppins">
            Acesse sua conta:
          </h2>

          {/* FORMULÁRIO DE LOGIN */}
          <form onSubmit={handleLogin} className="flex flex-col gap-5 w-full">

            {/* CAMPO EMAIL */}
            <div className="flex flex-col gap-2">
              <div className="flex items-center gap-2 text-[var(--color-primary)] font-semibold text-[16px] ml-2">
                <FaEnvelope className="text-lg" />
                <span>E-mail</span>
              </div>
              <Input
                hintText="Insira seu e-mail"
                type="email"
                value={email}
                onChange={setEmail}
                textColor="text-[var(--color-brown)] font-medium"
              />
            </div>

            {/* CAMPO SENHA */}
            <div className="flex flex-col gap-2">
              <div className="flex items-center gap-2 text-[var(--color-primary)] font-semibold text-[16px] ml-2">
                <FaLock className="text-lg" />
                <span>Senha</span>
              </div>
              <Input
                hintText="Insira sua senha"
                type="password"
                value={password}
                onChange={setPassword}
                textColor="text-[var(--color-brown)] font-medium"
              />
            </div>

            {/* ALERTA DE ERRO */}
            {errorMessage && (
              <div className="text-red-500 text-center font-semibold text-[14px] mt-2 transition-all duration-300">
                {errorMessage}
              </div>
            )}

            <div className="h-6" />

            {isLoading ? (
              <div className="flex flex-col items-center justify-center py-2">
                <div className="w-8 h-8 border-4 border-[var(--color-primary)] border-t-transparent rounded-full animate-spin"></div>
                <span className="text-xs font-semibold text-[var(--color-brown)] mt-2">Conectando...</span>
              </div>
            ) : (
              <div className="flex flex-col items-stretch">
                <button
                  type="submit"
                  className="flex items-center justify-center gap-2 h-[50px] bg-[var(--color-orange-900)] hover:brightness-110 active:scale-95 text-white font-bold text-lg rounded-full cursor-pointer shadow-md transition-all duration-300 font-poppins"
                >
                  Entrar
                </button>
                <button
                  type="button"
                  onClick={handleTestUserLogin}
                  className="mt-3 text-sm font-semibold text-[var(--color-primary)] hover:text-[var(--color-primary-active)] cursor-pointer text-center transition-all duration-300 focus:outline-none"
                >
                  Entrar com usuário teste
                </button>
              </div>
            )}
          </form>

          {/* MENSAGEM DO CADASTRO NO APP */}
          <div className="mt-8 flex flex-col items-center text-center">
            <p className="text-[12px] leading-snug text-[var(--color-orange-900)] font-semibold">
              Não tem uma conta? Realize o seu cadastro através do nosso aplicativo.
            </p>
          </div>

        </div>
      </div>

    </div>
  );
}
