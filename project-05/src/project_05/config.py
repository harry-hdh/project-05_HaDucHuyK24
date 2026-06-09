from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "glamira"
SOURCE_COLLECTION = "summary19"
# TARGET_COLLECTION = "ip_locations"


def get_mongo_client():
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        source_col = db[SOURCE_COLLECTION]
        print(f"Successfully connected to {db}.{source_col}.")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return

# get_mongo_client()