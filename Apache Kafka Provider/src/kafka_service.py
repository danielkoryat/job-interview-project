from confluent_kafka import Producer,Message
import os
from event import Event
import logging
from typing import Optional


class KafkaService:

    def __init__(self):
        #Initialize KafkaProducer with the topic name and a Kafka Producer instance.
        self.topic_name = os.getenv('TOPIC_NAME')
        if not self.topic_name:
            raise ValueError("TOPIC_NAME environment variable is not set.")
        self.producer = self.create_kafka_producer()

    def create_kafka_producer(self) -> Producer:
        #Creates and returns a configured Kafka Producer.
        conf = {
            'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
            'client.id': os.getenv('KAFKA_CLIENT_ID'),
        }
        if not conf['bootstrap.servers']:
            raise ValueError("KAFKA_BOOTSTRAP_SERVERS environment variable is not set.")
        return Producer(conf)
    
    @staticmethod
    def delivery_report(err : Optional[Exception], msg : Message):
        #Callback for Kafka message delivery reports.
        if err is not None:
            logging.error(f'Message delivery failed: {err}')
        else:
            logging.info(f'Message delivered to at offset {msg.offset()}') 

    def send_event_message(self):
        #Sends an event message to the Kafka topic.
        try:
            event = Event() 
            self.producer.produce(
                topic=self.topic_name,
                key=str(event.reporter_id),
                value=event.to_json(),
                callback=self.delivery_report
            )
            self.producer.poll(0) 
            logging.info(f"ebent id {event.reporter_id} sent successfully")
        except Exception as e:
            logging.error(f"An error occurred while sending the event message: {e}", exc_info=True)

    def flush(self):
        #Flushes the producer to ensure all messages are sent.
        self.producer.flush()
