package com.petdex.api.infrastructure.messaging.contracts;

public interface TelemetrySubscriberAsync {
    void subscribeAsync(String projectId, String subscriptionId);
}
