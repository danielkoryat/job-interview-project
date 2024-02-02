import time
import json
import os
from datetime import datetime
from mongo_service import MongoService 
from redis_service import RedisService  
from typing import Dict, Any, Tuple
from copy import deepcopy
import logging

def create_redis_key_value(record: Dict[str, Any]) -> Tuple[str, str]:
    #Converts a record to a Redis key-value pair.

    # Deep copy to prevent modifying the original record
    record_copy = deepcopy(record)
    record_copy['timestamp'] = record_copy['timestamp'].isoformat()

    key = f"{record_copy['reporter_id']}:{record_copy['timestamp']}"
    value = json.dumps(record_copy)
    return key, value

def process_records(mongo_service: MongoService, redis_service: RedisService):
    #Processes new records from MongoDB and saves them in Redis, returns the last processed timestamp.

    last_timestamp = redis_service.get_last_processed_timestamp()
    new_records = mongo_service.get_new_records(last_timestamp)

    if not new_records:
        logging.info("No new records to process")
        return

    for record in new_records:
        key, value = create_redis_key_value(record)
        is_inserted = redis_service.save_record(key, value)
        if is_inserted:
            logging.info(f"Inserted {key} into Redis")
            if record['timestamp'] > last_timestamp:
               last_timestamp = record['timestamp']
        else:
            logging.error(f"Failed to insert {key} into Redis")

    redis_service.save_last_processed_timestamp(last_timestamp)

def run_interval(interval: int): 
    #Runs the record processing at a specified interval.

    mongo_service = MongoService()
    redis_service = RedisService()

    while True:
        process_records(mongo_service, redis_service)
        time.sleep(interval)

def main():
    #Main function to set up and start the processing loop.

    interval = int(os.getenv('PROCESS_INTERVAL', 5))  # Default to 5 seconds
    logging.basicConfig(level=logging.INFO)
    run_interval(interval)

if __name__ == "__main__":
    main()
