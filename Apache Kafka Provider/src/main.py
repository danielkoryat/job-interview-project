import logging
import time
from kafka_service import KafkaService  

def main():
    #Main function to continuously send messages to Kafka.
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    kafka_service = KafkaService()

    try:
        logging.info("Starting to send messages to Kafka.")
        while True:
            kafka_service.send_event_message()
            time.sleep(1)  
    except KeyboardInterrupt:
        logging.info("Interrupted by user, shutting down.")
    finally:
        # Ensure all pending messages are sent and resources are released
        kafka_service.flush()
        logging.info("Kafka producer flushed and closed properly.")

if __name__ == '__main__':
    main()
