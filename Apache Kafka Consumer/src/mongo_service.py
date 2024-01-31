from pymongo import MongoClient
import os

class MongoService:
    def __init__(self):
        mongo_uri = os.getenv('MONGO_URI')
        self.client = MongoClient(mongo_uri)
        self.db = self.client[os.getenv('MONGO_DATABASE')]
        self.collection = self.db[os.getenv('MONGO_COLLECTION')]

    def insert_document(self, document):
        self.collection.insert_one(document)

    def test_connection(self):
        try:
           
            self.client.list_database_names()
            return True
        except Exception as e:
            print(f"Error testing MongoDB connection: {e}", flush=True)
            return False