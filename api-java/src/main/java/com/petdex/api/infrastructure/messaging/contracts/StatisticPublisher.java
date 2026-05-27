package com.petdex.api.infrastructure.messaging.contracts;

public interface StatisticPublisher {
    void publishEvent(String animalId, String tipoEvento);
}
