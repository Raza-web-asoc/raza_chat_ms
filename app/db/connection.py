import os
from pymongo import MongoClient
from dotenv import load_dotenv


load_dotenv()


MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = "chat_app"


client = MongoClient(MONGODB_URI)
db = client[DATABASE_NAME]
