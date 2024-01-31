from pymongo import MongoClient, database, collection
from datetime import datetime
from typing import Any, Iterator
import os
from utils import error_handler

class MongoService:
    @error_handler
    def __init__(self):        
        self.client: MongoClient = MongoClient(os.getenv('MONGO_URI'))
        self.db : database = self.client[os.getenv('MONGO_DATABASE')]
        self.collection : collection = self.db[os.getenv('MONGO_COLLECTION')]

    @error_handler
    def get_new_records(self, last_timestamp: datetime) -> Iterator[Any]:
        return self.collection.find({"timestamp": {"$gt": last_timestamp}}, {"_id": 0})
    