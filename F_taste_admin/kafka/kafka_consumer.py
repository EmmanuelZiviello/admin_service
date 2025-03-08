import os
from kafka import KafkaConsumer
import json
from F_taste_admin.services.admin_service import AdminService
from F_taste_admin.kafka.kafka_producer import send_kafka_message
# Percorso assoluto alla cartella dei certificati
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Ottiene la cartella dove si trova questo script
CERTS_DIR = os.path.join(BASE_DIR, "..", "certs")  # Risale di un livello e accede alla cartella "certs"

# Configurazione Kafka su Aiven e sui topic
KAFKA_BROKER_URL = "kafka-ftaste-kafka-ftaste.j.aivencloud.com:11837"



#consumer dedicato a ricevere richieste da altri servizi e chiamare metodi del service per svolgerle
consumer = KafkaConsumer(
    'admin.login.request',
    bootstrap_servers=KAFKA_BROKER_URL,
    client_id="admin_consumer",
    group_id="admin_service",
    security_protocol="SSL",
    ssl_cafile=os.path.join(CERTS_DIR, "ca.pem"),  # Percorso del certificato CA
    ssl_certfile=os.path.join(CERTS_DIR, "service.cert"),  # Percorso del certificato client
    ssl_keyfile=os.path.join(CERTS_DIR, "service.key"),  # Percorso della chiave privata
    auto_offset_reset="earliest",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

#consumer dedicato a ricevere solo risposte da altri servizi
consumer_response = KafkaConsumer(
    'patient.delete.success',
    'patient.delete.failed',
    'patient.getAll.success',
    'patient.getAll.failed',
    'dietitian.delete.success',
    'dietitian.delete.failed',
    'dietitian.getAll.success',
    'dietitian.getAll.failed',
    bootstrap_servers=KAFKA_BROKER_URL,
    client_id="admin_consumer",
    group_id="admin_service_response",
    security_protocol="SSL",
    ssl_cafile=os.path.join(CERTS_DIR, "ca.pem"),  # Percorso del certificato CA
    ssl_certfile=os.path.join(CERTS_DIR, "service.cert"),  # Percorso del certificato client
    ssl_keyfile=os.path.join(CERTS_DIR, "service.key"),  # Percorso della chiave privata
    auto_offset_reset="earliest",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)




def consume(app):
    #Ascolta Kafka e chiama il Service per la registrazione
    with app.app_context():
        for message in consumer:
            data = message.value
            topic=message.topic
          
            if topic == "admin.login.request":
                response,status=AdminService.login_admin(data)
                topic_producer="admin.login.success" if status == 200 else "admin.login.failed"
                send_kafka_message(topic_producer,response)
            
            
        