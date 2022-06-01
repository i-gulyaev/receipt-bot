from datetime import datetime
from hashlib import sha256
from typing import Any, Dict

from app.schemas import Receipt, ReceiptItem


def __parse_item(data) -> ReceiptItem:
    return ReceiptItem(
        name=data["name"],
        price=int(data["price"]) / 100.0,
        total_sum=int(data["sum"]) / 100.0,
        quantity=data["quantity"],
    )


def __parse_receipt_v1(
    data: Dict[str, Any],
) -> Receipt:
    seller = data["user"]
    total_sum = int(data["totalSum"]) / 100.0
    date = datetime.strptime(data["localDateTime"], "%Y-%m-%dT%H:%M")

    h = sha256()
    h.update(seller.encode())
    h.update(str(data["totalSum"]).encode())
    h.update(str(date.timestamp()).encode)
    id = h.hexdigest()

    items = []
    for item in data["items"]:
        items.append(__parse_item(item))

    return Receipt(
        id=id,
        seller=seller,
        total_sum=total_sum,
        date=date,
        items=items,
    )


def __parse_receipt_v2(
    data: Any,
) -> Receipt:
    id = data[0]["id"]
    seller = data[0]["seller"]["name"]
    total_sum = int(data[0]["query"]["sum"]) / 100.0
    date = datetime.strptime(data[0]["query"]["date"], "%Y-%m-%dT%H:%M")
    items = []

    for item in data[0]["ticket"]["document"]["receipt"]["items"]:
        items.append(__parse_item(item))

    return Receipt(
        id=id,
        seller=seller,
        total_sum=total_sum,
        date=date,
        items=items,
    )


def parse_receipt(
    data: Any,
) -> Receipt:
    if type(data) is list:
        return __parse_receipt_v2(data)
    else:
        return __parse_receipt_v1(data)


if __name__ == "__main__":
    import json
    import pathlib

    def load_receipts():
        result = []
        p = pathlib.Path("app/data")
        for f in p.iterdir():
            if f.is_file():
                with open(f) as handle:
                    result.append(parse_receipt(json.load(handle)))
        return result

    def main():
        print(load_receipts())

    main()
