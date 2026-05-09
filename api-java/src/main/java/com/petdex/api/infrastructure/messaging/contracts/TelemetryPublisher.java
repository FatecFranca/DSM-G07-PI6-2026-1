package com.petdex.api.infrastructure.messaging.contracts;

import com.petdex.api.application.contracts.dto.batimento.BatimentoPublisherDTO;
import com.petdex.api.application.contracts.dto.localizacao.LocalizacaoPublisherDTO;
import com.petdex.api.application.contracts.dto.movimento.MovimentoPublisherDTO;

public interface TelemetryPublisher {

    void publicarBatimento(BatimentoPublisherDTO batimento);
    void publicarLocalizacao(LocalizacaoPublisherDTO localizacao);
    void publicarMovimento(MovimentoPublisherDTO movimento);
}
