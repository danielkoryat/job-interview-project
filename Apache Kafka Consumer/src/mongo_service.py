import logging
from pymongo import MongoClient
import os
from utils import error_handler
from typing import Dict

class MongoService:
    
    @error_handler
    def __init__(self):
        #Initializes the MongoService with MongoDB connection and collection.
        mongo_uri = os.getenv('MONGO_URI')
        self.client = MongoClient(mongo_uri)
        self.db = self.client[os.getenv('MONGO_DATABASE')]
        self.collection = self.db[os.getenv('MONGO_COLLECTION')]
        logging.info("MongoDB connection established.")

    @error_handler
    def insert_document(self, document : Dict[str, any]):
        #Inserts a single document into the MongoDB collection.
        try:
            self.collection.insert_one(document)
            logging.info(f"Document inserted successfully: {document}")
        except Exception as e:
            logging.error(f"Error inserting document: {e}", exc_info=True)

    def setup_indexer(self):
        #Sets up an index for the collection based on the specified environment variable.
        index_key = os.getenv('MONGO_INDEX_KEY')
        if index_key:
            self.collection.create_index([(index_key, 1)]) 
            logging.info(f"Index created on key: {index_key}")
        else:
            logging.warning("No index key provided in environment variables.")
