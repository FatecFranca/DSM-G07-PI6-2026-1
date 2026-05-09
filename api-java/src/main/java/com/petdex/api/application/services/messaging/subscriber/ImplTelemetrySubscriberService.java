package com.petdex.api.application.services.messaging.subscriber;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.petdex.api.application.services.batimento.BatimentoService;
import com.petdex.api.application.services.localizacao.LocalizacaoService;
import com.petdex.api.application.services.movimento.MovimentoService;
import com.petdex.api.domain.contracts.dto.batimento.BatimentoPublisherDTO;
import com.petdex.api.domain.contracts.dto.batimento.BatimentoReqDTO;
import com.petdex.api.domain.contracts.dto.batimento.BatimentoResDTO;
import com.petdex.api.domain.contracts.dto.localizacao.LocalizacaoPublisherDTO;
import com.petdex.api.domain.contracts.dto.localizacao.LocalizacaoReqDTO;
import com.petdex.api.domain.contracts.dto.localizacao.LocalizacaoResDTO;
import com.petdex.api.domain.contracts.dto.movimento.MovimentoPublisherDTO;
import com.petdex.api.domain.contracts.dto.movimento.MovimentoReqDTO;
import com.petdex.api.domain.contracts.dto.movimento.MovimentoResDTO;
import com.petdex.api.domain.contracts.enums.TelemetryTypeEnum;
import lombok.AllArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class ImplTelemetrySubscriberService implements TelemetrySubscriberService {

    private final ObjectMapper mapper;
    private final BatimentoService batimentoService;
    private final LocalizacaoService localizacaoService;
    private final MovimentoService movimentoService;
    private static final Logger logger = LoggerFactory.getLogger(ImplTelemetrySubscriberService.class);

    @Override
    public boolean processarMensagem(String message) {
        try {

            JsonNode mensagemNode = mapper.readTree(message);
            JsonNode typeNode = mensagemNode.get("type");

            if (typeNode == null) {
                logger.error("[Telemetry Sub Service] Campo type não informado na mensagem");
                throw new IllegalArgumentException("[Telemetry Sub Service] Campo ´type´ não informado na mensagem");
            }

            String typeString = typeNode.asText();
            TelemetryTypeEnum type = TelemetryTypeEnum.fromString(typeString);

            switch (type) {
                case HEART_RATE:
                    BatimentoPublisherDTO batimento = mapper.treeToValue(mensagemNode, BatimentoPublisherDTO.class);
                    return this.processarBatimento(batimento);

                case LOCATION:
                    LocalizacaoPublisherDTO localizacao = mapper.treeToValue(mensagemNode, LocalizacaoPublisherDTO.class);
                    return this.processarLocalizacao(localizacao);

                case MOVEMENT:
                    MovimentoPublisherDTO movimento = mapper.treeToValue(mensagemNode, MovimentoPublisherDTO.class);
                    return this.processarMovimento(movimento);

                default:
                    logger.error("[Telemetry Subscriber Service] Tipo da mensagem desconhecido {}", type);
                    throw new IllegalArgumentException("Tipo de mensagem desconhecido" + type);
            }

        } catch (Exception e) {
            logger.error("[Telemetry Sub Service] Erro ao processar mensagem {}", e.getMessage());
            throw new RuntimeException("Erro ao processar a mensagem: ", e);
        }
    }


    private boolean processarBatimento(BatimentoPublisherDTO batimentoDTO) {
        logger.info("[Telemetry Sub Service] Batimento recebido: {}", batimentoDTO);
        try {
            BatimentoResDTO batimentoSalvo = batimentoService.save(mapper.convertValue(batimentoDTO, BatimentoReqDTO.class));
            if (batimentoSalvo == null) {
                logger.error("[Telemetry Sub Service] ERRO: batimento não foi cadastrado");
                return false;
            }
            logger.info("[Telemetry Sub Service] Sucesso: Batimento cadastrado!");
            return true;
        } catch (Exception exception) {
            return false;
        }
    }

    private boolean processarLocalizacao(LocalizacaoPublisherDTO localizacaoDTO) {
        logger.info("[Telemetry Sub Service] Localizacao recebida: {}", localizacaoDTO);
        try {
            LocalizacaoResDTO localizacaoSalva = localizacaoService.save(mapper.convertValue(localizacaoDTO, LocalizacaoReqDTO.class));
            if (localizacaoSalva == null) {
                logger.error("[Telemetry Sub Service] ERRO: localizacao não foi cadastrado");
                return false;
            }
            logger.info("[Telemetry Sub Service] Sucesso: Localizacao cadastrada!");
            return true;
        } catch (Exception exception) {
            return false;
        }
    }

    private boolean processarMovimento(MovimentoPublisherDTO movimentoDTO) {

        logger.info("[Telemetry Sub Service] Dados de movimento recebido: {}", movimentoDTO);
        try {
            MovimentoResDTO movimentoSalvo = movimentoService.save(mapper.convertValue(movimentoDTO, MovimentoReqDTO.class));
            if (movimentoSalvo == null) {
                logger.error("[Telemetry Sub Service] ERRO: Dados de movimento não foram cadastrados");
                return false;
            }
            logger.info("[Telemetry Sub Service] Sucesso: Movimento cadastrado!");
            return true;
        } catch (Exception exception) {
            return false;
        }
    }
}
