package com.petdex.api.application.services.mensageria.publisher;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.cloud.spring.pubsub.core.PubSubTemplate;

import com.petdex.api.domain.contracts.dto.batimento.BatimentoMensageriaReqDTO;
import com.petdex.api.domain.contracts.dto.localizacao.LocalizacaoMensageriaReqDTO;
import com.petdex.api.domain.contracts.dto.movimento.MovimentoMensageriaReqDTO;
import lombok.AllArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class ImplTelemetryPublisherService implements TelemetryPublisherService {

    private final String TOPIC = "petdex-telemetry";
    private final PubSubTemplate pubSubTemplate;
    private final ObjectMapper objectMapper;
    private static final Logger logger = LoggerFactory.getLogger(ImplTelemetryPublisherService.class);


    @Override
    public void publicarBatimento(BatimentoMensageriaReqDTO batimento) {
        try {
            logger.info("[Telemetry Publisher Service] Publicando batimento: {}", batimento);
            String batimentoJson = objectMapper.writeValueAsString(batimento);
            pubSubTemplate.publish(TOPIC, batimentoJson);
            logger.info("[Telemetry Publisher Service] Batimento publicado com sucesso!");
        } catch (JsonProcessingException e) {
            logger.error("[Telemetry Publisher Service] Erro ao converter batimento para JSON: {}", e.getMessage());
            throw new RuntimeException("Erro ao converter batimento para JSON", e);
        } catch (Exception e) {
            logger.error("[Telemetry Publisher Service] Erro publicar batimento: {}", e.getMessage());
            throw new RuntimeException("Erro ao publicar batimento", e);
        }
    }

    @Override
    public void publicarLocalizacao(LocalizacaoMensageriaReqDTO localizacao) {
        try {
            logger.info("[Telemetry Publisher Service] Publicando localizacao: {}", localizacao);
            String localizacaoJson = objectMapper.writeValueAsString(localizacao);
            pubSubTemplate.publish(TOPIC, localizacaoJson);
            logger.info("[Telemetry Publisher Service] Localizacao publicada com sucesso!");
        } catch (JsonProcessingException e) {
            logger.error("[Telemetry Publisher Service] Erro ao converter localizacao para JSON: {}", e.getMessage());
            throw new RuntimeException("Erro ao converter localizacao para JSON", e);
        }  catch (Exception e) {
            logger.error("[Telemetry Publisher Service] Erro publicar localizacao: {}", e.getMessage());
            throw new RuntimeException("Erro ao publicar localizacao", e);
        }
    }

    @Override
    public void publicarMovimento(MovimentoMensageriaReqDTO movimento) {
        try {
            logger.info("[Telemetry Publisher Service] Publicando movimento: {}", movimento);
            String localizacaoJson = objectMapper.writeValueAsString(movimento);
            pubSubTemplate.publish(TOPIC, localizacaoJson);
            logger.info("[Telemetry Publisher Service] Movimento publicado com sucesso!");
        } catch (JsonProcessingException e) {
            logger.error("[Telemetry Publisher Service] Erro ao converter movimento para JSON: {}", e.getMessage());
            throw new RuntimeException("Erro ao converter movimento para JSON", e);
        } catch (Exception e) {
            logger.error("[Telemetry Publisher Service] Erro publicar movimento: {}", e.getMessage());
            throw new RuntimeException("Erro ao publicar movimento", e);
        }
    }
}
