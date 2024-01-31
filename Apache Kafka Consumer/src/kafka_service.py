from confluent_kafka import Consumer, Message,KafkaError
from typing import Optional, Dict
import os
import json
from datetime import datetime
from utils import error_handler



class KafkaService:
    def __init__(self):
        self.consumer = self.create_kafka_consumer()

    def create_kafka_consumer(self) -> Consumer:
        consumer_config = {
            'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
            'group.id': os.getenv('CONSUMER_GROUP_ID'),
            'auto.offset.reset': os.getenv('AUTO_OFFSET_RESET'),
            'enable.auto.commit': False,  
        }
        consumer =  Consumer(consumer_config)
        consumer.subscribe([os.getenv('TOPIC_NAME')])
        return consumer
    
    @error_handler
    def consume_messages(self) -> Optional[Dict[str, any]]:
        msg = self.consumer.poll(8)
        if msg is None:
            print("No message received", flush=True)
            return None
         
        if msg.error():
            if not msg.error().code() == KafkaError._PARTITION_EOF:
                print(msg.error(), flush=True)
            else:
                print("End of partition event", flush=True)
            return None
        
        dict_for_database = self.process_message(msg)   
        return dict_for_database
    
    
    def process_message(self, msg: Message) -> Optional[Dict[str, any]]:
        try:
            self.consumer.commit(msg)
            decoded_message = msg.value().decode('utf-8')
            message_dict = json.loads(decoded_message)

            if 'timestamp' in message_dict:
                message_dict['timestamp'] = datetime.fromisoformat(message_dict['timestamp'])
            return message_dict

        except json.JSONDecodeError as e:
            print(f"Error processing message: {e}", flush=True)
