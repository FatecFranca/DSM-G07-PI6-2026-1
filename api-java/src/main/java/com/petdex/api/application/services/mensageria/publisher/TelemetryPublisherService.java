package com.petdex.api.application.services.mensageria.publisher;

import com.petdex.api.domain.contracts.dto.batimento.BatimentoMensageriaReqDTO;
import com.petdex.api.domain.contracts.dto.localizacao.LocalizacaoMensageriaReqDTO;
import com.petdex.api.domain.contracts.dto.movimento.MovimentoMensageriaReqDTO;

public interface TelemetryPublisherService {

    void publicarBatimento(BatimentoMensageriaReqDTO batimento);
    void publicarLocalizacao(LocalizacaoMensageriaReqDTO localizacao);
    void publicarMovimento(MovimentoMensageriaReqDTO movimento);
}
