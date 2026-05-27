package com.petdex.api.application.services.messaging.publisher;

import com.petdex.api.infrastructure.messaging.contracts.StatisticPublisher;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class ImplStatisticPublisherService implements StatisticPublisherService {

    private final StatisticPublisher statisticPublisher;

    @Override
    public void publishEvent(String animalId, String tipoEvento) {
        statisticPublisher.publishEvent(animalId, tipoEvento);
    }
}
