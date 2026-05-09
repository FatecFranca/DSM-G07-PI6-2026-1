package com.petdex.api.application.services.mensageria.publisher;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.cloud.spring.pubsub.core.PubSubTemplate;

import com.petdex.api.domain.contracts.dto.batimento.BatimentoMensageriaReqDTO;
import com.petdex.api.domain.contracts.dto.localizacao.LocalizacaoMensageriaReqDTO;
import com.petdex.api.domain.contracts.dto.movimento.MovimentoMensageriaReqDTO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
@Service
public class ImplPublisherService implements PublisherService {

    private final String TOPIC = "petdex-telemetry";

    @Autowired
    private PubSubTemplate pubSubTemplate;

    @Autowired
    private ObjectMapper objectMapper;

    public void publish(String mensagem) {
        pubSubTemplate.publish(TOPIC, mensagem);
    }

    @Override
    public void publicarBatimento(BatimentoMensageriaReqDTO batimento) {
        try {

            String batimentoJson = objectMapper.writeValueAsString(batimento);
            pubSubTemplate.publish(TOPIC, batimentoJson);

        } catch (JsonProcessingException e) {
            throw new RuntimeException("Erro ao converter batimento para JSON", e);
        }
    }

    @Override
    public void publicarLocalizacao(LocalizacaoMensageriaReqDTO localizacao) {
        try {
            String localizacaoJson = objectMapper.writeValueAsString(localizacao);
            pubSubTemplate.publish(TOPIC, localizacaoJson);
        } catch (JsonProcessingException e) {
            throw new RuntimeException("Erro ao converter localizacao para JSON", e);
        }
    }

    @Override
    public void publicarMovimento(MovimentoMensageriaReqDTO movimento) {
        try {
            String localizacaoJson = objectMapper.writeValueAsString(movimento);
            pubSubTemplate.publish(TOPIC, localizacaoJson);
        } catch (JsonProcessingException e) {
            throw new RuntimeException("Erro ao converter localizacao para JSON", e);
        }
    }
}
