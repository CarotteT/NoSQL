from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from config import MONGODB_URI

def get_mongo_connection():
    uri = MONGODB_URI

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)
        return None

def get_mongo_collection():
    client = get_mongo_connection()
    if client:
        db = client.entertainment
        return db.films
    return None

client = get_mongo_connection()

"""
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from config import MONGO_URI

uri = MONGO_URI

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Sélection de la base et de la collection
db = client.entertainment
films = db.films
"""

