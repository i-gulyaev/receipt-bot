import datetime

from receipt_bot.util import create_document, create_receipt_id


def test_create_receipt_id():

    receipt = {
        "seller": "AAAAA",
        "sum": 42.42,
        "date": datetime.datetime(2020, 1, 1, 10, 10, 10),
    }

    expected_id = (
        "cf94e930b8d92aae97c6c0281925b7c60a0a8f815548f1b93616100c07dce9c9"
    )

    assert expected_id == create_receipt_id(receipt)


def test_create_document():

    receipt = {
        "seller": "AAAAA",
        "sum": 42.42,
        "date": datetime.datetime(2020, 1, 1, 10, 10, 10),
    }

    raw_data = "BBBBB"

    expected_doc = {
        "id": create_receipt_id(receipt),
        "date": receipt["date"].timestamp(),
        "status": 0,
        "sum": receipt["sum"],
        "seller": receipt["seller"],
        "raw_data": raw_data,
    }

    assert expected_doc == create_document(receipt, raw_data)
