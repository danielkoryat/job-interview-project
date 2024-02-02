from kafka_service import KafkaService
from mongo_service import MongoService
import time
import logging
from utils import error_handler

def main():
    #Main function to consume messages from Kafka and insert them into MongoDB.
    kafka_service = KafkaService()
    mongo_service = MongoService()
    mongo_service.setup_indexer()

    try:
        while True:
            document = kafka_service.consume_messages()
            if document:
                mongo_service.insert_document(document)
                kafka_service.consumer.commit()
                logging.info(f"Message ID: {document['reporter_id']} inserted successfully")
            time.sleep(1)
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
    finally:
        kafka_service.consumer.close()
        logging.info("Kafka consumer closed.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
