from hashlib import sha256
from typing import Any, Dict, List


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


def stringify_item(date, item: Dict[str, Any], label) -> str:
    name = item["name"].replace(";", ".")
    item_sum = item["sum"]
    return f"{date};{label};{name};{item_sum}"


def format_messages(
    receipt: Dict[str, Any],
    labels: List[str],
    message_size: int,
) -> List[str]:
    result = []
    date = receipt["date"].strftime("%Y-%m-%d")

    message = ""

    items = [
        stringify_item(date, item, label)
        for item, label in zip(receipt["items"], labels)
    ]

    for item in items:
        if (len(message) + len(item) + 1) > message_size:
            result.append(message)
            message = ""
        message += item + "\n"

    if message:
        result.append(message)

    return result
