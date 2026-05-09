package com.petdex.api.infrastructure.messaging;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.petdex.api.application.services.mensageria.subscriber.TelemetrySubscriberService;
import com.petdex.api.domain.contracts.dto.batimento.BatimentoMensageriaReqDTO;
import com.petdex.api.domain.contracts.dto.localizacao.LocalizacaoMensageriaReqDTO;
import com.petdex.api.domain.contracts.dto.movimento.MovimentoMensageriaReqDTO;
import com.petdex.api.domain.contracts.enums.TelemetryTypeEnum;
import lombok.AllArgsConstructor;
import org.slf4j.LoggerFactory;
import org.slf4j.Logger;
import org.springframework.stereotype.Service;


@AllArgsConstructor
@Service
public class TelemetrySubscriber {

    private final ObjectMapper mapper;
    private final TelemetrySubscriberService telemetrySubscriberService;
    private static final Logger logger = LoggerFactory.getLogger(TelemetrySubscriber.class);

    public Boolean receiveMessage(String message) {
        try {

            logger.info("[Telemetry Subcriber] Menssagem recebida: {}", message);
            JsonNode mensagemNode = mapper.readTree(message);
            JsonNode typeNode = mensagemNode.get("type");

            if (typeNode == null) {
                logger.error("[Telemetry Subcriber] Campo type não informado na mensagem");
                throw new IllegalArgumentException("[Telemetry Subcriber] Campo ´type´ não informado na mensagem");
            }

            String typeString = typeNode.asText();
            TelemetryTypeEnum type = TelemetryTypeEnum.fromString(typeString);

            switch (type) {
                case HEART_RATE:
                    BatimentoMensageriaReqDTO batimento = mapper.treeToValue(mensagemNode, BatimentoMensageriaReqDTO.class);
                    return telemetrySubscriberService.processarBatimento(batimento);

                case LOCATION:
                    LocalizacaoMensageriaReqDTO localizacao = mapper.treeToValue(mensagemNode, LocalizacaoMensageriaReqDTO.class);
                    return telemetrySubscriberService.processarLocalizacao(localizacao);

                case MOVEMENT:
                    MovimentoMensageriaReqDTO movimento = mapper.treeToValue(mensagemNode, MovimentoMensageriaReqDTO.class);
                    return telemetrySubscriberService.processarMovimento(movimento);

                default:
                    logger.error("[Telemetry Subcriber] Tipo da mensagem desconhecido {}", type);
                    throw new IllegalArgumentException("Tipo de mensagem desconhecido" + type);
            }

        } catch (Exception e) {
            logger.error("[Telemetry Subcriber] Erro ao processar mensagem {}", e.getMessage());
           throw new RuntimeException("Erro ao processar a mensagem: ", e);
        }
    }
}
