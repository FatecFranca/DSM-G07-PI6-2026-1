package com.petdex.api.infrastructure.messaging;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.cloud.spring.pubsub.core.PubSubTemplate;
import com.petdex.api.infrastructure.messaging.contracts.StatisticPublisher;
import lombok.AllArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.Map;

@Service
@AllArgsConstructor
public class StatisticPublisherPubSub implements StatisticPublisher {

    private final String TOPIC = "petdex-statistic";
    private final PubSubTemplate pubSubTemplate;
    private final ObjectMapper objectMapper;
    private static final Logger logger = LoggerFactory.getLogger(StatisticPublisherPubSub.class);

    @Override
    public void publishEvent(String animalId, String tipoEvento) {
        try {
            Map<String, String> payload = new HashMap<>();
            payload.put("animal_id", animalId);
            payload.put("tipo_evento", tipoEvento);
            
            String json = objectMapper.writeValueAsString(payload);
            logger.info("Publicando evento estatístico: {}", json);
            pubSubTemplate.publish(TOPIC, json);
        } catch (JsonProcessingException e) {
            logger.error("Erro ao serializar evento estatístico", e);
        } catch (Exception e) {
            logger.error("Erro ao publicar evento estatístico", e);
        }
    }
}
