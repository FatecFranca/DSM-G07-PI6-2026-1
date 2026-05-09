package com.petdex.api.application.services.messaging.publisher;

import com.petdex.api.domain.contracts.dto.batimento.BatimentoPublisherDTO;
import com.petdex.api.domain.contracts.dto.localizacao.LocalizacaoPublisherDTO;
import com.petdex.api.domain.contracts.dto.movimento.MovimentoPublisherDTO;

public interface TelemetryPublisherService {

    void processarBatimento(BatimentoPublisherDTO batimentoPublisherDTO);
    void processarMovimento(MovimentoPublisherDTO movimentoPublisherDTO);
    void processarLocalizacao(LocalizacaoPublisherDTO localizacaoPublisherDTO);
}
