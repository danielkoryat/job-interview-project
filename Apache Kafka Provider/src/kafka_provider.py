import logging
import os
import time
from confluent_kafka import Producer
from event import Event

def delivery_report(err, msg):
    #Callback function for Kafka message delivery.
    if err is not None:
        logging.error(f'Message delivery failed: {err}')
    else:
        logging.info(f'Message delivered to {msg.topic()}')

def create_kafka_producer():
    #Creates and configures a Kafka producer.
    conf = {
        'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
        'client.id': os.getenv('KAFKA_CLIENT_ID'),
    }
    return Producer(conf)

def main():
    #Main function to produce events and send them to Kafka.
    producer = create_kafka_producer()

    try:
        while True:
            event = Event()
            topic_name = os.getenv('TOPIC_NAME')
            if not topic_name:
                logging.error("TOPIC_NAME environment variable is not set.")
                break
            producer.produce(topic=topic_name, key=str(event.reporter_id), value=event.to_json(), callback=delivery_report)
            producer.poll(0)
            time.sleep(1)  
    except KeyboardInterrupt:
        logging.info("Interrupted by user, shutting down.")
    finally:
        producer.flush()
        logging.info("Kafka producer flushed and closed.")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
