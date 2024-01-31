import redis
import os
from typing import Any
from datetime import datetime
from utils import error_handler

class RedisService:
    @error_handler
    def __init__(self):
        redis_host = os.getenv('REDIS_HOST')
        redis_port = int(os.getenv('REDIS_PORT', '6379'))
        self.client: redis.Redis = redis.Redis(host=redis_host, port=redis_port)

    @error_handler
    def save_record(self, key: str, value: Any) -> bool:
        return self.client.set(key, value)
    
    @error_handler
    def save_last_processed_timestamp(self, timestamp: datetime) -> bool:
        return self.client.set('last_processed_timestamp', timestamp.isoformat())
    
    @error_handler
    def get_last_processed_timestamp(self) -> datetime:
        last_processed_timestamp = self.client.get('last_processed_timestamp')
        if last_processed_timestamp:
            return datetime.fromisoformat(last_processed_timestamp.decode('utf-8'))
        else:
            return datetime.min