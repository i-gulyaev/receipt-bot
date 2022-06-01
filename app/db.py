from typing import Any, Dict

from pymongo import MongoClient

from app.schemas import Receipt


def create_document(receipt: Receipt, data: Any) -> Dict[str, Any]:
    return {
        "id": receipt.id,
        "date": receipt.date.timestamp(),
        "status": 0,
        "sum": receipt.total_sum,
        "seller": receipt.seller,
        "raw_data": data,
    }


class Connector:
    def __init__(self, uri: str, name: str, collection: str):
        self._client = MongoClient(uri)
        self._db = self._client[name]
        self._collection = self._db[collection]

    def add_document(self, doc: Dict[str, Any]):
        key = {"id": doc["id"]}
        self._collection.update_one(key, {"$set": doc}, upsert=True)
