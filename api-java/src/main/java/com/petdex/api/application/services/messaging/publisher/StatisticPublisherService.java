package com.petdex.api.application.services.messaging.publisher;

public interface StatisticPublisherService {
    void publishEvent(String animalId, String tipoEvento);
}
