from pymongo import MongoClient
from pymongo.collection import Collection

from app.config import settings


client = MongoClient(settings.mongodb_uri)

database = client[settings.mongodb_database]

publications: Collection = database[
    settings.mongodb_collection
]


def create_indexes() -> None:
    """ MongoDB automatically creates a unique index on _id"""
    pass


def close_connection() -> None:
    client.close()