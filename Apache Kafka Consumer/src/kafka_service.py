import logging
from confluent_kafka import Consumer, KafkaError,Message
import os
import json
from datetime import datetime,timezone
from typing import Optional, Dict
from utils import error_handler

class KafkaService:
    def __init__(self):
        self.consumer = self.create_kafka_consumer()

    def create_kafka_consumer(self) -> Consumer:
        #Creates and configures a Kafka consumer.
        consumer_config = {
            'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
            'group.id': os.getenv('CONSUMER_GROUP_ID'),
            'auto.offset.reset': os.getenv('AUTO_OFFSET_RESET'),
            'enable.auto.commit': False,  
        }
        consumer = Consumer(consumer_config)
        consumer.subscribe([os.getenv('TOPIC_NAME')])
        return consumer
    
    @error_handler
    def consume_messages(self) -> Optional[Dict[str, any]]:
        #Consumes messages from Kafka, returning a dictionary for database storage.
        msg = self.consumer.poll(5) 

        if msg is None:
            logging.info("No message received")
            return None
         
        if msg.error():
            if msg.error().code() != KafkaError._PARTITION_EOF:
                logging.error(msg.error())
            else:
                logging.info("End of partition event")
            return None
        
        document_for_database = self.process_message(msg)   
        return document_for_database

    def process_message(self, msg : Message) -> Optional[Dict[str, any]]:
        #Processes the Kafka message and returns a dictionary.
        try:
            self.consumer.commit(msg)
            decoded_message = msg.value().decode('utf-8')
            message_dict = json.loads(decoded_message)

            if 'timestamp' in message_dict:
                message_dict['timestamp'] = datetime.fromisoformat(message_dict['timestamp'].rstrip('Z')).replace(tzinfo=timezone.utc)
            return message_dict

        except json.JSONDecodeError as e:
            logging.error(f"Error processing message: {e}")
            return None
