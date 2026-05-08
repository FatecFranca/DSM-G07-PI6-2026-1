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
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class ImplTelemetrySubscriberService implements TelemetrySubscriberService {

    private final ObjectMapper mapper;
    private final BatimentoService batimentoService;
    private final LocalizacaoService localizacaoService;
    private final MovimentoService movimentoService;

    @Override
    public boolean processarBatimento(BatimentoMensageriaReqDTO batimentoDTO) {
        System.out.println("[Telemetry Sub Service] Batimento recebido: " + batimentoDTO);
        try {
            BatimentoResDTO batimentoSalvo = batimentoService.save(mapper.convertValue(batimentoDTO, BatimentoReqDTO.class));
            if (batimentoSalvo == null) {
                System.out.println("[Telemetry Sub Service] ERRO: localizacao não foi cadastrado");
                return false;
            }
            System.out.println("[Telemetry Sub Service] Sucesso: Batimento cadastrado!");
            return true;
        } catch (Exception exception) {
            return false;
        }
    }

    @Override
    public boolean processarLocalizacao(LocalizacaoMensageriaReqDTO localizacaoDTO) {
        System.out.println("[Telemetry Sub Service] Localizacao recebida: " + localizacaoDTO);
        try {
            LocalizacaoResDTO localizacaoSalva = localizacaoService.save(mapper.convertValue(localizacaoDTO, LocalizacaoReqDTO.class));
            if (localizacaoSalva == null) {
                System.out.println("[Telemetry Sub Service] ERRO: localizacao não foi cadastrado");
                return false;
            }
            System.out.println("[Telemetry Sub Service] Sucesso: Localizacao cadastrada!");
            return true;
        } catch (Exception exception) {
            return false;
        }
    }

    @Override
    public boolean processarMovimento(MovimentoMensageriaReqDTO movimentoDTO) {

        System.out.println("[Telemetry Sub Service] Dados de movimento recebido: " + movimentoDTO);
        try {
            MovimentoResDTO movimentoSalvo = movimentoService.save(mapper.convertValue(movimentoDTO, MovimentoReqDTO.class));
            if (movimentoSalvo == null) {
                System.out.println("[Telemetry Sub Service] ERRO: Dados de movimento não foram cadastrados");
                return false;
            }
            System.out.println("[Telemetry Sub Service] Sucesso: Movimento cadastrado!");
            return true;
        } catch (Exception exception) {
            return false;
        }
    }
}
