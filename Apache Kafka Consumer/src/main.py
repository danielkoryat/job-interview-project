from kafka_service import KafkaService
from mongo_service import MongoService
import time


kafka_service = KafkaService()
mongo_service = MongoService()

if __name__ == "__main__":  
    try:
        while True:
            document = kafka_service.consume_messages()
            if document:
                mongo_service.insert_document(document)
                kafka_service.consumer.commit()
                print(f"message ID: {document['id']} inserted successfully", flush=True)
            time.sleep(1)
    except Exception as e:
        print(e)
        kafka_service.consumer.close()

    
