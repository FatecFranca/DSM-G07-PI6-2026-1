package com.petdex.api.infrastructure.messaging.interfaces;

import com.petdex.api.domain.contracts.dto.batimento.BatimentoPublisherDTO;
import com.petdex.api.domain.contracts.dto.localizacao.LocalizacaoPublisherDTO;
import com.petdex.api.domain.contracts.dto.movimento.MovimentoPublisherDTO;

public interface TelemetryPublisher {

    void publicarBatimento(BatimentoPublisherDTO batimento);
    void publicarLocalizacao(LocalizacaoPublisherDTO localizacao);
    void publicarMovimento(MovimentoPublisherDTO movimento);
}
