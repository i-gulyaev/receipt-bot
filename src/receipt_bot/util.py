from hashlib import sha256
from typing import Any, Dict


def create_receipt_id(receipt: Dict[str, Any]):
    h = sha256()
    h.update(str(receipt["seller"]).encode())
    h.update(str(receipt["sum"]).encode())
    h.update(str(receipt["date"].timestamp()).encode())
    return h.hexdigest()


def create_document(receipt: Dict[str, Any], data: Any) -> Dict[str, Any]:

    return {
        "id": create_receipt_id(receipt),
        "date": receipt["date"].timestamp(),
        "status": 0,
        "sum": receipt["sum"],
        "seller": receipt["seller"],
        "raw_data": data,
    }
