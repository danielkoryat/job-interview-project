from pymongo import MongoClient
import os
from typing import Iterator, Any
from datetime import datetime
from utils import error_handler
import logging

class MongoService:
    @error_handler
    def __init__(self):        
        #Initializes a MongoDB service with connection to the specified database and collection.
        mongo_uri = os.getenv('MONGO_URI')
        if not mongo_uri:
            logging.error("MONGO_URI environment variable is not set.")
            return
        self.client: MongoClient = MongoClient(mongo_uri)
        self.db = self.client[os.getenv('MONGO_DATABASE')]
        self.collection = self.db[os.getenv('MONGO_COLLECTION')]

    @error_handler
    def get_new_records(self, last_timestamp: datetime) -> Iterator[Any]:
        #Fetches new records from the collection that are newer than the given timestamp. 
        query = {"timestamp": {"$gt": last_timestamp}}
        cleaning_instractions = {"_id": 0}  # Exclude the MongoDB '_id' field
        return self.collection.find(query, cleaning_instractions).sort("timestamp", 1)
