package com.petdex.api.infrastructure.websocket;

import com.petdex.api.application.contracts.websocket.NotificationService;
import com.petdex.api.application.contracts.dto.websocket.BatimentoWebSocketDTO;
import com.petdex.api.application.contracts.dto.websocket.LocalizacaoWebSocketDTO;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Component;

import java.util.concurrent.atomic.AtomicLong;

@Component
public class WebSocketNotificationAdapter implements NotificationService {

    @Autowired
    private SimpMessagingTemplate messagingTemplate;

    private static final Logger logger = LoggerFactory.getLogger(WebSocketNotificationAdapter.class);
    private final AtomicLong contadorLocalizacao = new AtomicLong(0);
    private final AtomicLong contadorBatimento = new AtomicLong(0);

    @Override
    public void enviarNotificacaoLocalizacao(String animalId, LocalizacaoWebSocketDTO localizacaoDTO) {
        long numeroMensagem = contadorLocalizacao.incrementAndGet();
        String topico = "/topic/animal/" + animalId;

        logger.info("[WebSocket Adapter] [ENVIO #{}] Enviando notificação de localização para o animal: {}", numeroMensagem, animalId);
        messagingTemplate.convertAndSend(topico, localizacaoDTO);
        logger.info("[WebSocket Adapter] Mensagem enviada com sucesso para o tópico: {}", topico);
    }

    @Override
    public void enviarNotificacaoBatimento(String animalId, BatimentoWebSocketDTO batimentoDTO) {
        long numeroMensagem = contadorBatimento.incrementAndGet();
        String topico = "/topic/animal/" + animalId;

        logger.info("[WebSocket Adapter] [ENVIO #{}] Enviando notificação de batimento para o animal: {}", numeroMensagem, animalId);
        messagingTemplate.convertAndSend(topico, batimentoDTO);
        logger.info("[WebSocket Adapter] Mensagem enviada com sucesso para o tópico: {}", topico);
    }
}
