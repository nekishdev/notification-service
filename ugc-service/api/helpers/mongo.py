import pymongo
from settings import settings

mongo_client = pymongo.MongoClient(settings.MONGO_DSN, uuidRepresentation="standard")

mongo = mongo_client["content"]


def ensure_collections_exists() -> None:
    names = ["film_scores", "films", "reviews"]
    collections = mongo.list_collection_names()

    for name in names:
        if name not in collections:
            mongo.create_collection(name)
