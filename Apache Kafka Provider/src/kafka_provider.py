from confluent_kafka import Producer
import time
from Event import Event
import os

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

# Kafka configuration
conf = {
        'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
        'client.id': os.getenv('KAFKA_CLIENT_ID'),
}

producer = Producer(conf)

try:
    if __name__ == '__main__':
        while True:
            event = Event()
            producer.produce('event', key=str(event.id), value=event.to_json(), callback=delivery_report)
            producer.poll(0)
            time.sleep(1)  
except KeyboardInterrupt:
    pass
finally:
    producer.flush()

