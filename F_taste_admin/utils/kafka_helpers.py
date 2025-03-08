from F_taste_admin.kafka.kafka_consumer import consumer_response

def wait_for_kafka_response(topics):
    for message in consumer_response:
        if message.topic in topics:
            return message.value