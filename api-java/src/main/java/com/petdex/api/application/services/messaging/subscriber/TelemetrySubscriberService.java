package com.petdex.api.application.services.messaging.subscriber;


public interface TelemetrySubscriberService {
    boolean processarMensagem(String message);
}
