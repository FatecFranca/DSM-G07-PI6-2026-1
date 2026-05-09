package com.petdex.api.application.services.mensageria.subscriber;

import com.petdex.api.domain.contracts.dto.batimento.BatimentoMensageriaReqDTO;
import com.petdex.api.domain.contracts.dto.localizacao.LocalizacaoMensageriaReqDTO;
import com.petdex.api.domain.contracts.dto.movimento.MovimentoMensageriaReqDTO;


public interface TelemetrySubscriberService {
    boolean processarMensagem(String message);
}
