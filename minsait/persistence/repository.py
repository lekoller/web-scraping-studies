from datetime import datetime
from pymongo import MongoClient, DESCENDING

class GenericRepository:
    def __init__(self, db_name, collection_name):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def get_last_document(self):
        return self.collection.find_one(sort=[('_id', DESCENDING)])

    def insert_document(self, document):
        self.collection.insert_one(document)

        

    def remove_document(self, id):
        self.collection.delete_one({'_id': id})
