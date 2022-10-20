import time
from datetime import datetime
from functools import wraps
from pprint import pprint
from random import randint
from uuid import uuid4

from pymongo import MongoClient
from pymongo.collection import Collection

MONGO_HOST = "mongo"
MONGO_DB = "movieDb"
MONGO_COLLECTION = "film_likes"
film = "4879be63-4371-45ac-a58c-a1a3c02dc71b"


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__} {kwargs} Took {total_time:.4f} seconds')
        return result

    return timeit_wrapper


def get_like_event() -> dict:
    """Генерация события like."""
    return {
        "user_id": str(uuid4()),
        "film_id": film,  # str(uuid4()),
        "like": randint(0, 10),
        "date": datetime.utcnow()
    }


class ReasearchMongoDB:
    def __init__(self) -> None:
        """Init."""
        self.client = MongoClient(MONGO_HOST)
        self.db = self.client[MONGO_DB]

    @timeit
    def select_avg_like_film(self, name_collection: str) -> None:
        _collection: Collection = self.db[name_collection]
        pipeline = [
            {"$match": {"film_id": film}},
            {"$group": {"_id": "film_id", "avg_like": {"$avg": "$like"}}}
        ]
        pprint(list(_collection.aggregate(pipeline)))

    @timeit
    def select_count_like_film(self, name_collection: str, ) -> None:
        _collection: Collection = self.db[name_collection]
        pipeline = [
            {"$match": {"film_id": film}},
            {"$group": {"_id": "film_id", "count_like": {"$sum": 1}}}
        ]
        pprint(list(_collection.aggregate(pipeline)))

    def insert(self, name_collection: str, document) -> None:
        _collection = self.db[name_collection]
        _collection.insert_one(document)


if __name__ == "__main__":
    mongo = ReasearchMongoDB()
    i = 1
    while True:
        doc = get_like_event()
        mongo.insert(MONGO_COLLECTION, doc)
        if i == 1_000 or i == 10_000 or i == 100_000 or i == 1_000_000:
            mongo.select_avg_like_film(MONGO_COLLECTION)
            mongo.select_count_like_film(MONGO_COLLECTION)
        i += 1
