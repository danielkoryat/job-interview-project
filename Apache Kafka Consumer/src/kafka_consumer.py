from confluent_kafka import Consumer, KafkaException, KafkaError
import json


topic_name = 'event'  
group_id = 'order_processing_group'

def create_kafka_consumer(topic_name, group_id):
    consumer_config = {
        'bootstrap.servers': "kafka:9092",
        'group.id': group_id,
        'auto.offset.reset': 'latest',
        'enable.auto.commit': False,  # Manual offset commit
    }
    consumer = Consumer(consumer_config)
    consumer.subscribe([topic_name])
    return consumer

def consume_messages(consumer):
    try:
        while True:
            msg = consumer.poll(5)  
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    continue
                else:
                    print(msg.error())
                    break
            decoded_message = msg.value().decode('utf-8')
            message_dict = json.loads(decoded_message)
            print(f"message ID: {message_dict['id']} create at {message_dict['timestamp']}", flush=True)
            consumer.commit(msg)  
    except KeyboardInterrupt:
        print("Stopping consumer...")
    finally:
        consumer.close()

if __name__ == "__main__":
    consumer = create_kafka_consumer( topic_name, group_id)
    consume_messages(consumer)