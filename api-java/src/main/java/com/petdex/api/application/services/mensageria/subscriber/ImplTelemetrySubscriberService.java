package com.petdex.api.application.services.mensageria.subscriber;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.petdex.api.application.services.batimento.BatimentoService;
import com.petdex.api.application.services.localizacao.LocalizacaoService;
import com.petdex.api.application.services.movimento.MovimentoService;
import com.petdex.api.domain.contracts.dto.batimento.BatimentoMensageriaReqDTO;
import com.petdex.api.domain.contracts.dto.batimento.BatimentoReqDTO;
import com.petdex.api.domain.contracts.dto.batimento.BatimentoResDTO;
import com.petdex.api.domain.contracts.dto.localizacao.LocalizacaoMensageriaReqDTO;
import com.petdex.api.domain.contracts.dto.localizacao.LocalizacaoReqDTO;
import com.petdex.api.domain.contracts.dto.localizacao.LocalizacaoResDTO;
import com.petdex.api.domain.contracts.dto.movimento.MovimentoMensageriaReqDTO;
import com.petdex.api.domain.contracts.dto.movimento.MovimentoReqDTO;
import com.petdex.api.domain.contracts.dto.movimento.MovimentoResDTO;
import com.petdex.api.infrastructure.messaging.TelemetrySubscriber;
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
    public boolean processarBatimento(BatimentoMensageriaReqDTO batimentoDTO) {
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

    @Override
    public boolean processarLocalizacao(LocalizacaoMensageriaReqDTO localizacaoDTO) {
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

    @Override
    public boolean processarMovimento(MovimentoMensageriaReqDTO movimentoDTO) {

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
