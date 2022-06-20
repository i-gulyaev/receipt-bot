import datetime

from receipt_bot import util


def test_create_receipt_id():

    receipt = {
        "seller": "AAAAA",
        "sum": 42.42,
        "date": datetime.datetime(2020, 1, 1, 10, 10, 10),
    }

    expected_id = (
        "cf94e930b8d92aae97c6c0281925b7c60a0a8f815548f1b93616100c07dce9c9"
    )

    assert expected_id == util.create_receipt_id(receipt)


def test_create_document():

    receipt = {
        "seller": "AAAAA",
        "sum": 42.42,
        "date": datetime.datetime(2020, 1, 1, 10, 10, 10),
    }

    raw_data = "BBBBB"

    expected_doc = {
        "id": util.create_receipt_id(receipt),
        "date": receipt["date"].timestamp(),
        "status": 0,
        "sum": receipt["sum"],
        "seller": receipt["seller"],
        "raw_data": raw_data,
    }

    assert expected_doc == util.create_document(receipt, raw_data)


def test_stringify_item():

    date_str = datetime.datetime(2020, 1, 1).strftime("%Y-%m-%d")

    item = {
        "name": "BBBBB",
        "price": 21.21,
        "sum": 42.42,
        "quantity": 2,
    }

    label = "Fruits"

    expected = "{};{};{};{}".format(date_str, label, item["name"], item["sum"])

    assert expected == util.stringify_item(date_str, item, label)


def test_format_message():

    item = {
        "name": "BBBBB",
        "price": 21.21,
        "sum": 42.42,
        "quantity": 2,
    }

    receipt = {
        "seller": "AAAAA",
        "sum": 42.42,
        "date": datetime.datetime(2020, 1, 1, 10, 10, 10),
        "items": [item],
    }

    labels = ["Fruits"]
    msg_size = 2048

    msg_content = (
        util.stringify_item(
            receipt["date"].strftime("%Y-%m-%d"),
            item,
            labels[0],
        )
        + "\n"
    )

    result = util.format_messages(receipt, labels, msg_size)
    assert 1 == len(result)
    assert [msg_content] == result


def test_format_long_message():
    item = {
        "name": "BBBBB",
        "price": 21.21,
        "sum": 42.42,
        "quantity": 2,
    }

    num_items = 10
    receipt = {
        "seller": "AAAAA",
        "sum": 42.42,
        "date": datetime.datetime(2020, 1, 1, 10, 10, 10),
        "items": num_items * [item],
    }

    labels = num_items * ["Fruits"]

    msg_content = (
        util.stringify_item(
            receipt["date"].strftime("%Y-%m-%d"),
            item,
            labels[0],
        )
        + "\n"
    )

    # this is to ensure record is not splitted across multiple messages
    msg_size = len(msg_content) * 1.5

    result = util.format_messages(receipt, labels, msg_size)
    assert num_items == len(result)
    for msg in result:
        assert msg_content == msg
