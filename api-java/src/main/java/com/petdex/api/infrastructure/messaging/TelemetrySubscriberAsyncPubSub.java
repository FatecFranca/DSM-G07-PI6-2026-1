package com.petdex.api.infrastructure.messaging;

import com.google.cloud.spring.pubsub.core.PubSubTemplate;
import com.petdex.api.application.services.messaging.subscriber.TelemetrySubscriberService;
import com.petdex.api.infrastructure.messaging.contracts.TelemetrySubscriberAsync;
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
    private PubSubTemplate pubSubTemplate;

    @Autowired
    private TelemetrySubscriberService telemetrySubscriberService;

    private Logger logger = LoggerFactory.getLogger(TelemetrySubscriberAsyncPubSub.class);

    public void run(String... args) throws Exception {
        String subscriptionId = "petdex-telemetry-sub";
        subscribeAsync(this.projectId, subscriptionId);
    }

    @Override
    public void subscribeAsync(String projectId, String subscriptionId) {
        try {
            logger.info("Iniciando escuta assíncrona da subscrição: {}", subscriptionId);
            pubSubTemplate.subscribe(subscriptionId, message -> {
                String messageId = message.getPubsubMessage().getMessageId();
                try {
                    logger.info("Mensagem recebida. ID: {}", messageId);
                    String data = message.getPubsubMessage().getData().toStringUtf8();
                    if (!telemetrySubscriberService.processarMensagem(data)) {
                        logger.error("Erro ao processar a mensagem. ID: {}", messageId);
                        message.nack();
                    } else {
                        logger.info("Mensagem processada com sucesso. ID: {}", messageId);
                        message.ack();
                    }
                } catch (Exception e) {
                    logger.error("Exceção ao processar mensagem ID: {}. Erro: {}", messageId, e.getMessage());
                    message.nack();
                }
            });
            logger.info("Subscription iniciada com sucesso para: {}", subscriptionId);
        } catch (Exception exception) {
            logger.error("Erro ao iniciar subscrição {}: {}", subscriptionId, exception.getMessage());
        }
    }
}
