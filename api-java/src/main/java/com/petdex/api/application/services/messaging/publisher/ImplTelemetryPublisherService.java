package com.petdex.api.application.services.messaging.publisher;

import com.petdex.api.application.contracts.dto.batimento.BatimentoPublisherDTO;
import com.petdex.api.application.contracts.dto.localizacao.LocalizacaoPublisherDTO;
import com.petdex.api.application.contracts.dto.movimento.MovimentoPublisherDTO;
import com.petdex.api.infrastructure.messaging.contracts.TelemetryPublisher;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class ImplTelemetryPublisherService implements TelemetryPublisherService {

    private final TelemetryPublisher telemetryPublisher;

    @Override
    public void processarBatimento(BatimentoPublisherDTO batimentoPublisherDTO) {
        telemetryPublisher.publicarBatimento(batimentoPublisherDTO);
    }

    @Override
    public void processarMovimento(MovimentoPublisherDTO movimentoPublisherDTO) {
        telemetryPublisher.publicarMovimento(movimentoPublisherDTO);
    }

    @Override
    public void processarLocalizacao(LocalizacaoPublisherDTO localizacaoPublisherDTO) {
        telemetryPublisher.publicarLocalizacao(localizacaoPublisherDTO);
    }
}
