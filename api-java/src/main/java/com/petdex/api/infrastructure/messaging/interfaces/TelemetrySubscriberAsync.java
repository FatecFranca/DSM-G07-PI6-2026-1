package com.petdex.api.infrastructure.messaging.interfaces;

public interface TelemetrySubscriberAsync {
    void subscribeAsync(String projectId, String subscriptionId);
}
