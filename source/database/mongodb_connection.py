from pymongo import MongoClient
import os

class MongoDBConnection():

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBConnection, cls).__new__(cls)
            
            host = os.getenv("MONGO_HOST")
            username = os.getenv("MONGO_USERNAME")
            password = os.getenv("MONGO_PASSWORD")
            uri = f"mongodb+srv://{username}:{password}@{host}/?retryWrites=true&w=majority&appName=DrinkWater"
        
            cls._instance.client = MongoClient(uri)
        return cls._instance

    def get_client(self):
        return self.client