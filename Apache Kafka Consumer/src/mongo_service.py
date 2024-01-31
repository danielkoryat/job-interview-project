from pymongo import MongoClient
import os
from utils import error_handler

class MongoService:

    @error_handler
    def __init__(self):
        mongo_uri = os.getenv('MONGO_URI')
        self.client = MongoClient(mongo_uri)
        self.db = self.client[os.getenv('MONGO_DATABASE')]
        self.collection = self.db[os.getenv('MONGO_COLLECTION')]

    @error_handler
    def insert_document(self, document):
        self.collection.insert_one(document)