package com.petdex.api.infrastructure.messaging;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.cloud.spring.pubsub.core.PubSubTemplate;

import com.petdex.api.domain.contracts.dto.batimento.BatimentoPublisherDTO;
import com.petdex.api.domain.contracts.dto.localizacao.LocalizacaoPublisherDTO;
import com.petdex.api.domain.contracts.dto.movimento.MovimentoPublisherDTO;
import com.petdex.api.infrastructure.messaging.interfaces.TelemetryPublisher;
import lombok.AllArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class TelemetryPublisherPubSub implements TelemetryPublisher {

    private final String TOPIC = "petdex-telemetry";
    private final PubSubTemplate pubSubTemplate;
    private final ObjectMapper objectMapper;
    private static final Logger logger = LoggerFactory.getLogger(TelemetryPublisherPubSub.class);

    @Override
    public void publicarBatimento(BatimentoPublisherDTO batimento) {
        try {
            logger.info("Publicando batimento: {}", batimento);
            String batimentoJson = objectMapper.writeValueAsString(batimento);
            pubSubTemplate.publish(TOPIC, batimentoJson);
            logger.info("Batimento publicado com sucesso!");
        } catch (JsonProcessingException e) {
            logger.error("Erro ao converter batimento para JSON: {}", e.getMessage());
            throw new RuntimeException("Erro ao converter batimento para JSON", e);
        } catch (Exception e) {
            logger.error("Erro publicar batimento: {}", e.getMessage());
            throw new RuntimeException("Erro ao publicar batimento", e);
        }
    }

    @Override
    public void publicarLocalizacao(LocalizacaoPublisherDTO localizacao) {
        try {
            logger.info("Publicando localizacao: {}", localizacao);
            String localizacaoJson = objectMapper.writeValueAsString(localizacao);
            pubSubTemplate.publish(TOPIC, localizacaoJson);
            logger.info("Localizacao publicada com sucesso!");
        } catch (JsonProcessingException e) {
            logger.error("Erro ao converter localizacao para JSON: {}", e.getMessage());
            throw new RuntimeException("Erro ao converter localizacao para JSON", e);
        }  catch (Exception e) {
            logger.error("Erro publicar localizacao: {}", e.getMessage());
            throw new RuntimeException("Erro ao publicar localizacao", e);
        }
    }

    @Override
    public void publicarMovimento(MovimentoPublisherDTO movimento) {
        try {
            logger.info("Publicando movimento: {}", movimento);
            String localizacaoJson = objectMapper.writeValueAsString(movimento);
            pubSubTemplate.publish(TOPIC, localizacaoJson);
            logger.info("Movimento publicado com sucesso!");
        } catch (JsonProcessingException e) {
            logger.error("Erro ao converter movimento para JSON: {}", e.getMessage());
            throw new RuntimeException("Erro ao converter movimento para JSON", e);
        } catch (Exception e) {
            logger.error("Erro publicar movimento: {}", e.getMessage());
            throw new RuntimeException("Erro ao publicar movimento", e);
        }
    }
}
