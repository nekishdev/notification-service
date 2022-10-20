from typing import Any, Generator

import pprint
import random
import time
from uuid import uuid4

import pymongo
from bson import ObjectId
from pymongo.database import Database


def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb://root:example@localhost:27017"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = pymongo.MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['content']


def reviews_generator(collection: pymongo.collection.Collection, batch_count: int, batch_size: int) -> Generator[Any, Any, None]:
    def generate_sentence() -> str:
        names = ["We", "I", "They", "He", "She", "Jack", "Jim"]
        verbs = ["was", "is", "are", "were"]
        nouns = ["playing a game", "watching television", "talking", "dancing", "speaking"]

        return names[random.randrange(0, len(names) - 1)] \
            + " " + verbs[random.randrange(0, len(verbs) - 1)] \
            + " " \
            + nouns[random.randrange(0, len(nouns) - 1)]

    for _ in range(0, batch_count):
        collection_items = [{"text": generate_sentence()} for _ in range(0, batch_size)]
        insert_result = collection.insert_many(collection_items)
        yield insert_result.inserted_ids


def add_scores(collection: pymongo.collection.Collection, reviews_ids: list[str], count: int) -> None:
    def create_score_doc(_review_id):
        score = random.randint(0, 1)
        score = 10 if score == 1 else 0
        return {
            "review_id": _review_id,
            "score": score,
            "user_id": str(uuid4())
        }

    collection_items = []
    for review_id in reviews_ids:
        collection_items.extend([create_score_doc(review_id) for _ in range(0, count)])

    collection.insert_many(collection_items)


def run(_db: Database) -> None:
    reviews_batch_count = 100
    reviews_batch_size = 10000
    scores_count = random.randint(5, 10)
    reviews_collection = db["reviews"]
    scores_collection = db["scores"]

    for reviews_ids in reviews_generator(reviews_collection, reviews_batch_count, reviews_batch_size):
        print("reviews added")
        add_scores(scores_collection, reviews_ids, scores_count)
        print("scores added\n\n")


def test_selects(_db: Database) -> None:
    start = time.monotonic()
    collection = _db["scores"]
    pipeline = [
        {"$match": {"review_id": ObjectId("633ff747344459feb4cfd4f7")}},
        {
            "$lookup": {
                "from": "reviews",
                "localField": "review_id",
                "foreignField": "_id",
                "as": "review_object"
            }
        },
        {"$group": {"_id": "review_id", "totalCount": {"$count": {}}}}
    ]
    cursor = collection.aggregate(pipeline)
    pprint.pprint(cursor.next())

    duration = time.monotonic() - start
    pprint.pprint({"time: ": duration})


db = get_database()

test_selects(db)
