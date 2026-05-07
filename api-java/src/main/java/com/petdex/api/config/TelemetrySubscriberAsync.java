package com.petdex.api.config;

import com.google.cloud.pubsub.v1.AckReplyConsumer;
import com.google.cloud.pubsub.v1.MessageReceiver;
import com.google.cloud.pubsub.v1.Subscriber;
import com.google.pubsub.v1.ProjectSubscriptionName;
import com.google.pubsub.v1.PubsubMessage;
import com.petdex.api.infrastructure.messaging.TelemetrySubscriber;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;


@Component
public class TelemetrySubscriberAsync implements CommandLineRunner {

    @Value("${spring.cloud.gcp.project-id}")
    String projectId;

    @Autowired
    private TelemetrySubscriber telemetrySubscriber;

    public void run(String... args) throws Exception {
        String subscriptionId = "petdex-telemetry-sub";
        //subscribeAsync(this.projectId, subscriptionId);
    }

//    private void subscribeAsync(String projectId, String subscriptionId) {
//        ProjectSubscriptionName subscriptionName = ProjectSubscriptionName.of(projectId, subscriptionId);
//
//        MessageReceiver receiver = (PubsubMessage message, AckReplyConsumer consumer) -> {
//            String data = message.getData().toStringUtf8();
//            System.out.println("ACK: " + data);
//            if(!telemetrySubscriber.receiveMessage(data)) {
//                consumer.ack();
//            }
//
//            consumer.ack();
//        };
//
//        Subscriber subscriber = null;
//        try {
//            subscriber = Subscriber.newBuilder(subscriptionName, receiver).build();
//            subscriber.startAsync().awaitRunning();
//            System.out.println("Escutando mensagem: " + subscriptionName);
//            try {
//                Thread.currentThread().join();
//            } catch (InterruptedException e) {
//                Thread.currentThread().interrupt();
//                System.err.println("Thread interrompido: " + e.getMessage());
//            }
//        } catch (Exception exception) {
//            if (subscriber != null) {
//                subscriber.stopAsync();
//            }
//        }
//    }
}
