package com.petdex.api.infrastructure.messaging;

import com.google.cloud.pubsub.v1.AckReplyConsumer;
import com.google.cloud.pubsub.v1.MessageReceiver;
import com.google.cloud.pubsub.v1.Subscriber;
import com.google.pubsub.v1.ProjectSubscriptionName;
import com.google.pubsub.v1.PubsubMessage;
import com.petdex.api.application.services.messaging.subscriber.TelemetrySubscriberService;
import com.petdex.api.infrastructure.messaging.interfaces.TelemetrySubscriberAsync;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;


@Component
public class TelemetrySubscriberAsyncPubSub implements CommandLineRunner, TelemetrySubscriberAsync {

    @Value("${spring.cloud.gcp.project-id}")
    String projectId;

    @Autowired
    private TelemetrySubscriberService telemetrySubscriberService;

    private Logger logger = LoggerFactory.getLogger(TelemetrySubscriberAsyncPubSub.class);


    public void run(String... args) throws Exception {
        String subscriptionId = "petdex-telemetry-sub";
        subscribeAsync(this.projectId, subscriptionId);
    }

    @Override
     public void subscribeAsync(String projectId, String subscriptionId) {
        ProjectSubscriptionName subscriptionName = ProjectSubscriptionName.of(projectId, subscriptionId);

        MessageReceiver receiver = (PubsubMessage message, AckReplyConsumer consumer) -> {
            try {
                logger.info("[Telemetry Sub Async] Mensagem recebida. ID: {}", message.getMessageId());
                String data = message.getData().toStringUtf8();
                if(!telemetrySubscriberService.processarMensagem(data)) {
                    logger.error("[Telemetry Sub Async] Erro ao processar a mensagem. ID: {}", message.getMessageId());
                    consumer.nack();
                } else {
                    logger.info("[Telemetry Sub Async] Mensagem processada com sucesso. ID: {}", message.getMessageId());
                    consumer.ack();
                }
            } catch (Exception e) {
                logger.error("[Telemetry Sub Async] Exceção ao processar mensagem ID: {}. Erro: {}", message.getMessageId(), e.getMessage());
                consumer.nack();
            }
        };

        Subscriber subscriber = null;
        try {
            subscriber = Subscriber.newBuilder(subscriptionName, receiver).build();
            subscriber.startAsync().awaitRunning();
            logger.info("[Telemetry Sub Async] Subscription iniciada: {}", subscriptionName);
            try {
                Thread.currentThread().join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                logger.error("[Telemetry Sub Async] Thread interrompido: {}", e.getMessage());
            }
        } catch (Exception exception) {
            logger.error("[Telemetry Sub Async] Erro: {}", exception.getMessage());
            if (subscriber != null) {
                subscriber.stopAsync();
            }
        }
    }
}
