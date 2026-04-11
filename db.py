import certifi
from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://anamtamujeeb17_db_user:AAn93eB0bwcqjAHX@cluster0.jvjfdv4.mongodb.net/?appName=Cluster0",
    tlsCAFile=certifi.where()
)
db = client["sentiment_app"]

users_collection = db["users"]
history_collection = db["history"]