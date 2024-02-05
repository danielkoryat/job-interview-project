import time
from mongo_service import MongoService 
from redis_service import RedisService  
import logging


def process_records(mongo_service: MongoService, redis_service: RedisService):
    # Processes new records from MongoDB and saves them in Redis.
    last_timestamp = redis_service.get_last_processed_timestamp()
    new_records = mongo_service.get_new_records(last_timestamp)

    if not new_records:
        logging.info("No new records to process")
        return

    for record in new_records:
        key, value = redis_service.create_redis_key_value(record)
        # Prepare a dictionary for the current key-value pair and the last processed timestamp
        redis_updates = {key: value}
        last_timestamp = record['timestamp']
        redis_updates['last_processed_timestamp'] = last_timestamp.isoformat()

        is_success = redis_service.save_record(redis_updates)
        if is_success:
            logging.info(f"Updated Redis with key: {key}")
        else:
            logging.error(f"Failed to update Redis with key: {key}")

def run_interval(): 
    #Runs the record processing at a specified interval.

    mongo_service = MongoService()
    redis_service = RedisService()


    while True:
        process_records(mongo_service, redis_service)
        time.sleep(5)

def main():
    #Main function to set up and start the processing loop.

    logging.basicConfig(level=logging.INFO,format='%(levelname)s - %(message)s')
    run_interval()

if __name__ == "__main__":
    main()
