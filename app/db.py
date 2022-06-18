from hashlib import sha256
from typing import Any, Dict

from pymongo import MongoClient


def _id_from_receipt(receipt: Dict[str, Any]):
    h = sha256()
    h.update(str(receipt["seller"]).encode())
    h.update(str(receipt["sum"]).encode())
    h.update(str(receipt["date"].timestamp()).encode())
    return h.hexdigest()


def create_document(receipt: Dict[str, Any], data: Any) -> Dict[str, Any]:

    return {
        "id": _id_from_receipt(receipt),
        "date": receipt["date"].timestamp(),
        "status": 0,
        "sum": receipt["sum"],
        "seller": receipt["seller"],
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


def main():
    import datetime

    r = {"seller": "AAA", "sum": 10.11, "date": datetime.datetime.now()}

    print(_id_from_receipt(r))


if __name__ == "__main__":
    main()
