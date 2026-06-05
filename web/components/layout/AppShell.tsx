"use client";

import { useEffect, useState } from "react";

import MapScreen from "@/components/screens/MapScreen/MapScreen";
import LocationScreen from "@/components/screens/LocationScreen/LocationScreen";
import HealthScreen from "@/components/screens/HealthScreen/HealthScreen";
import CheckupScreen from "@/components/screens/CheckupScreen/CheckupScreen";
import LoginScreen from "@/components/screens/LoginScreen/LoginScreen";
import BottomNavWithStatus from "@/components/ui/BottomNavWithStatus";

import { getAnimalData } from "@/services/animalService";
import { connectWebSocket, subscribe, subscribeConnection } from "@/services/websocketService";
import { authService } from "@/services/authService";

export default function AppShell() {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
  const [currentIndex, setCurrentIndex] = useState(0);

  const [lastBpm, setLastBpm] = useState<number | null>(null);
  const [isConnected, setIsConnected] = useState(false);

  const [animalId, setAnimalId] = useState("");
  const [petName, setPetName] = useState("Pet");
  const [animalImagemUrl, setAnimalImagemUrl] = useState<string | null>(null);

  // 🔄 Carrega sessão salva no storage no primeiro render
  useEffect(() => {
    async function initAuth() {
      console.log("[AppShell] Inicializando AuthService...");
      try {
        await authService.init();
        const authenticated = authService.isAuthenticated();
        setIsAuthenticated(authenticated);
        if (authenticated) {
          setAnimalId(authService.getAnimalId() || "");
          setPetName(authService.getPetName() || "Pet");
          setAnimalImagemUrl(authService.getAnimalImagemUrl() || null);
        }
      } catch (err) {
        console.error("[AppShell] Erro ao carregar AuthService:", err);
        setIsAuthenticated(false);
      }
    }
    initAuth();
  }, []);

  const handleLoginSuccess = () => {
    setIsAuthenticated(true);
    setAnimalId(authService.getAnimalId() || "");
    setPetName(authService.getPetName() || "Pet");
    setAnimalImagemUrl(authService.getAnimalImagemUrl() || null);
  };

  const handleLogout = () => {
    console.log("[AppShell] Saindo da conta...");
    authService.logout();
    setIsAuthenticated(false);
    setAnimalId("");
    setPetName("Pet");
    setAnimalImagemUrl(null);
    setLastBpm(null);
    setCurrentIndex(0);
  };

  // 📡 WS connection reactive on animalId
  useEffect(() => {
    if (!animalId) return;

    // Inicializa a conexão do WebSocket de forma global para o animal
    connectWebSocket(animalId);

    const unsubscribeConnection = subscribeConnection((status) => {
      setIsConnected(status);
    });

    const unsubscribeTelemetry = subscribe((data) => {
      const payload = data.payload || data;
      const wsAnimalId = payload.animalId || payload.animal || data.animalId || data.animal;

      if (wsAnimalId === animalId) {
        if (payload.tipo === "batimento" || payload.frequenciaMedia !== undefined) {
          console.log("❤️ [AppShell] BPM atualizado via WS:", payload.frequenciaMedia);
          setLastBpm(payload.frequenciaMedia);
        }
      }
    });

    return () => {
      unsubscribeConnection();
      unsubscribeTelemetry();
    };
  }, [animalId]);

  // 🐶 Reactive animal profile load
  useEffect(() => {
    if (!animalId) return;

    async function loadAnimal() {
      console.log("🐶 Buscando dados do animal:", animalId);
      try {
        const animal = await getAnimalData(animalId);
        console.log("📦 Resposta animal:", animal);

        if (animal?.bpm != null) {
          console.log("❤️ SETANDO BPM:", animal.bpm);
          setLastBpm(animal.bpm);
        } else {
          console.log("❌ BPM veio null/undefined");
        }

        if (animal?.urlImagem) {
          console.log("🖼️ SETANDO IMAGEM ANIMAL:", animal.urlImagem);
          setAnimalImagemUrl(animal.urlImagem);
        }
      } catch (err) {
        console.error("Erro ao carregar dados do pet:", err);
      }
    }

    loadAnimal();
  }, [animalId]);

  // ⌛ RENDERIZANDO SPINNER DE CARREGAMENTO DE SESSÃO
  if (isAuthenticated === null) {
    return (
      <div className="w-screen h-screen bg-[var(--color-sand-100)] flex flex-col items-center justify-center gap-4">
        <div className="w-10 h-10 border-4 border-[var(--color-orange-900)] border-t-transparent rounded-full animate-spin"></div>
        <span className="text-xs font-bold text-[var(--color-brown)] uppercase tracking-widest opacity-70">
          Carregando sessão...
        </span>
      </div>
    );
  }

  // 🔒 RENDERIZANDO TELA DE LOGIN SE NÃO AUTENTICADO
  if (!isAuthenticated) {
    return <LoginScreen onLoginSuccess={handleLoginSuccess} />;
  }

  const pages = [
    <MapScreen
      key="map"
      setLastBpm={setLastBpm}
      animalId={animalId}
      animalName={petName}
      animalImagemUrl={animalImagemUrl}
      onLogout={handleLogout}
    />,
    <HealthScreen
      key="health"
      animalId={animalId}
      animalName={petName}
    />,
    <CheckupScreen
      key="checkup"
      animalId={animalId}
      animalName={petName}
    />,
    <LocationScreen
      key="location"
      animalId={animalId}
      animalName={petName}
    />,
  ];

  return (
    <div className="h-screen overflow-hidden">
      {pages[currentIndex]}

      <BottomNavWithStatus
        currentIndex={currentIndex}
        onChange={setCurrentIndex}
        lastBpm={lastBpm}
        isConnected={isConnected}
        animalId={animalId}
        animalName={petName}
        animalImagemUrl={animalImagemUrl}
      />
    </div>
  );
}