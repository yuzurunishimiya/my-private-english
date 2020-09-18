from pymongo import MongoClient
import os

client = MongoClient(os.environ.get("MONGO_URI", "mongodb://127.0.0.1:27017/"))
database = client['english_club']
db_vocabulary = database.vocabulary
db_users = database.users
