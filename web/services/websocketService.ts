import { Client } from "@stomp/stompjs";
import SockJS from "sockjs-client";

const WEBSOCKET_URL = process.env.NEXT_PUBLIC_WEBSOCKET_URL?.trim() || "";

let client: Client;

type Callback = (data: any) => void;

const listeners: Callback[] = [];
const connectionListeners: ((isConnected: boolean) => void)[] = [];

function notifyConnection(status: boolean) {
  connectionListeners.forEach((cb) => cb(status));
}

export function connectWebSocket(animalId: string) {
  if (client?.active) {
    console.log("🟡 WebSocket já conectado");
    return;
  }

  console.log("🔌 Conectando WebSocket...");
  console.log("🌐 URL:", WEBSOCKET_URL);

  client = new Client({
    webSocketFactory: () => new SockJS(WEBSOCKET_URL),

    reconnectDelay: 5000,

    onConnect: () => {
      notifyConnection(true);
      console.log("🟢 STOMP conectado");
      console.log(`📡 Inscrito em /topic/animal/${animalId}`);

      client.subscribe(`/topic/animal/${animalId}`, (message) => {
        try {
          const data = JSON.parse(message.body);

          console.log("📩 WS recebido:", data);

          listeners.forEach((cb) => cb(data));
        } catch (e) {
          console.error("❌ Erro ao processar WS:", e);
        }
      });
    },

    onStompError: (frame) => {
      console.error("❌ STOMP erro:", frame);
    },

    onDisconnect: () => {
      notifyConnection(false);
      console.log("🔴 STOMP desconectado");
    },

    onWebSocketClose: () => {
      notifyConnection(false);
      console.log("🔌 WebSocket fechado");
    },

    onWebSocketError: (event) => {
      console.error("❌ WebSocket erro:", event);
    },
  });

  client.activate();
}

export function subscribe(callback: Callback) {
  listeners.push(callback);

  console.log("👂 Novo listener registrado");

  return () => {
    const index = listeners.indexOf(callback);
    if (index > -1) {
      listeners.splice(index, 1);
      console.log("🔇 Listener removido");
    }
  };
}

export function subscribeConnection(callback: (isConnected: boolean) => void) {
  connectionListeners.push(callback);
  callback(client?.active ?? false);

  return () => {
    const index = connectionListeners.indexOf(callback);
    if (index > -1) {
      connectionListeners.splice(index, 1);
    }
  };
}