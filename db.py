import certifi
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(
    MONGO_URI,
    tlsCAFile=certifi.where()
)

db = client["sentiment_app"]

users_collection = db["users"]
history_collection = db["history"]