import time
import json
import os
from datetime import datetime
from mongo_service import MongoService 
from redis_service import RedisService  
from typing import Dict, Any, Tuple
from copy import deepcopy


def create_redis_key_value(record: Dict[str, Any]) -> Tuple[str, str]:
    # convert timestamp to ISO format
    record_copy = deepcopy(record)
    record_copy['timestamp'] = record_copy['timestamp'].isoformat()

    # Creates a unique key and JSON string value for each record
    key = f"{record_copy['reporterId']}:{record_copy['timestamp']}"
    value = json.dumps(record_copy)
    return key, value

def process_records(mongo_service: MongoService, redis_service: RedisService) -> datetime:
    # Process new records from MongoDB and save them in Redis
    last_timestamp = redis_service.get_last_processed_timestamp()
    new_records = mongo_service.get_new_records(last_timestamp)

    if new_records:
        print(f"Found new records {new_records}", flush=True)
        for record in new_records:
            key, value = create_redis_key_value(record)
            isInserted = redis_service.save_record(key, value)
            if isInserted:
                print(f"Inserted {key} into Redis", flush=True)
                if record['timestamp'] > last_timestamp:
                   last_timestamp = record['timestamp']
            else:
                print(f"Failed to insert {key} into Redis", flush=True)
    else:
        print("No new records found", flush=True)

    # Save the last processed timestamp to Redis
    redis_service.save_last_processed_timestamp(last_timestamp)
    return last_timestamp

def run_interval(interval: int): 
    # Initialize MongoDB and Redis services
    mongo_service = MongoService()
    redis_service = RedisService()

    # Continuously process records at specified intervals
    while True:
        process_records(mongo_service, redis_service)
        time.sleep(interval)

def main():
    # Set the interval for processing records and start the loop
    interval = 5
    run_interval(interval)

if __name__ == "__main__":
    main()
