from typing import Any, Dict

from pymongo import MongoClient


class Connector:
    def __init__(self, uri: str, name: str, collection: str):
        self._client = MongoClient(uri)
        self._db = self._client[name]
        self._collection = self._db[collection]

    def add_document(self, doc: Dict[str, Any]):
        key = {"id": doc["id"]}
        self._collection.update_one(key, {"$set": doc}, upsert=True)
