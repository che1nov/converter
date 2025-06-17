import os
from pymongo import MongoClient
from pymongo.collection import Collection
from dotenv import load_dotenv


class HistoryManager:
    def __init__(
        self,
        mongo_client=None,
        db_name="currency_converter",
        collection_name="history",
    ):
        load_dotenv()
        if mongo_client is None:
            mongo_uri = os.environ.get(
                "MONGODB_URI", "mongodb://localhost:27017/"
            )
            self.client = MongoClient(mongo_uri)
        else:
            self.client = mongo_client

        self.db = self.client[db_name]
        self.collection: Collection = self.db[collection_name]

    def add_operation(self, operation):
        self.collection.insert_one(operation)

    def get_operations(self):
        operations = list(self.collection.find({}, {"_id": 0}))
        return operations
