import redis
import os
from typing import Any
from datetime import datetime
import logging
from utils import error_handler
import json
from copy import deepcopy
from typing import Tuple, Dict


class RedisService:
    @error_handler
    def __init__(self):
        #Initializes a Redis service with connection to the specified Redis server.
        redis_host = os.getenv('REDIS_HOST')
        if not redis_host:
            logging.error("REDIS_HOST environment variable is not set.")
            raise ValueError("REDIS_HOST environment variable is not set.")

        redis_port = int(os.getenv('REDIS_PORT', '6379'))  # Default to 6379 if not set
        self.client: redis.Redis = redis.Redis(host=redis_host, port=redis_port)

    def save_record(self, updates: dict) -> bool:
    # Saves a record in Redis
    # return: True if the operation was successful, False otherwise.
        try:
            return self.client.mset(updates)
        except Exception as e:
            logging.error(f"Failed to update Redis with error: {e}")
            return False

    
    @error_handler
    def get_last_processed_timestamp(self) -> datetime:
        #Retrieves the last processed timestamp from Redis.
        last_processed_timestamp = self.client.get('last_processed_timestamp')
        if last_processed_timestamp:
            return datetime.fromisoformat(last_processed_timestamp.decode('utf-8'))
        else:
            return datetime.min
        
    def create_redis_key_value(self,record: Dict[str, Any]) -> Tuple[str, str]:
    #Converts a record to a Redis key-value pair.

    # Deep copy to prevent modifying the original record
        record_copy = deepcopy(record)
        record_copy['timestamp'] = record_copy['timestamp'].isoformat()

        key = f"{record_copy['reporter_id']}:{record_copy['timestamp']}"
        value = json.dumps(record_copy)
        return key, value
