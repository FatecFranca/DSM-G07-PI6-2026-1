import { Client } from "@stomp/stompjs";
import SockJS from "sockjs-client";

const WEBSOCKET_URL = process.env.NEXT_PUBLIC_WEBSOCKET_URL!;

let client: Client;

type Callback = (data: any) => void;

const listeners: Callback[] = [];

export function connectWebSocket() {
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
      console.log("🟢 STOMP conectado");
      console.log("📡 Inscrito em /topic/petdex");

      client.subscribe("/topic/petdex", (message) => {
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
      console.log("🔴 STOMP desconectado");
    },

    onWebSocketClose: () => {
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
}