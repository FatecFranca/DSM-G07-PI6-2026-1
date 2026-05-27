import os
import json
import logging
import threading
from google.cloud import pubsub_v1
from app.application.services.estatistica_service import EstatisticaService
from app.application.services.jwt_service import jwt_service

logger = logging.getLogger("PubSubConsumer")

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    try:
        data = json.loads(message.data.decode("utf-8"))
        logger.info(f"Mensagem recebida: {data}")
        animal_id = data.get("animal_id")
        tipo_evento = data.get("tipo_evento")

        if animal_id and tipo_evento:
            token = jwt_service.generate_token(user_id="system-pubsub", email="system@petdex.com")
            bearer_token = f"Bearer {token}"
            
            estatistica_service = EstatisticaService()
            
            if tipo_evento == "BATIMENTO":
                estatistica_service.batimentos_calcular_estatisticas(animal_id, bearer_token)
                estatistica_service.media_ultimos_5_dias_validos(animal_id, bearer_token)
                estatistica_service.media_ultimas_5_horas_registradas(animal_id, bearer_token)
                estatistica_service.analise_regressao_batimentos(animal_id, bearer_token)
            elif tipo_evento == "MOVIMENTO":
                estatistica_service.analise_regressao_batimentos(animal_id, bearer_token)
                
        message.ack()
    except Exception as e:
        logger.error(f"Erro ao processar mensagem do Pub/Sub: {e}")
        message.nack()

def run_consumer():
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "petdex-project")
    subscription_id = os.environ.get("PUBSUB_SUBSCRIPTION", "petdex-statistic-sub")
    
    try:
        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = subscriber.subscription_path(project_id, subscription_id)
        
        streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
        logger.info(f"Inscrito em {subscription_path} aguardando mensagens...")
        
        try:
            streaming_pull_future.result()
        except Exception as e:
            streaming_pull_future.cancel()
            streaming_pull_future.result()
    except Exception as e:
        logger.error(f"Erro ao iniciar PubSub consumer: {e}")

def start_pubsub_consumer():
    thread = threading.Thread(target=run_consumer, daemon=True)
    thread.start()
