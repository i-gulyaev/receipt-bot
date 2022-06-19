import json
import logging
import pathlib
from typing import Any, Dict, List

import i18n
from goodsclf.classifier import GoodsClassifier
from receipt_parser import parse_receipt
from telebot import TeleBot
from telebot import logger as tb_logger
from telebot import types

from .db import Connector
from .settings import settings
from .util import create_document

logger = tb_logger
tb_logger.setLevel(logging.DEBUG)

here = pathlib.Path(__file__).parent.resolve()

i18n.load_path.append(here / "i18n")
i18n.set("locale", "ru")
i18n.set("fallback", "en")

MAX_MESSAGE_SIZE = 4096


def stringify_item(date, item: Dict[str, Any], label) -> str:
    name = item["name"].replace(";", ".")
    item_sum = item["sum"]
    return f"{date};{label};{name};{item_sum}"


def format_messages(
    receipt: Dict[str, Any],
    clf: GoodsClassifier,
    message_size: int = MAX_MESSAGE_SIZE,
) -> List[str]:
    result = []
    date = receipt["date"].strftime("%Y-%m-%d")

    message = ""

    item_names = [item["name"] for item in receipt["items"]]

    items = [
        stringify_item(date, item, label)
        for item, label in zip(receipt["items"], clf.predict(item_names))
    ]

    for item in items:
        if (len(message) + len(item) + 1) > message_size:
            result.append(message)
            message = ""
        message += item + "\n"

    if message:
        result.append(message)

    return result


def process_receipt(
    bot: TeleBot,
    message: types.Message,
    connector: Connector,
    clf: GoodsClassifier,
):
    assert message.document
    try:
        file_info = bot.get_file(message.document.file_id)
        content = bot.download_file(file_info.file_path)

        content = json.loads(content)
        logger.debug(f"Get file={file_info}, content={content}")
        receipt = parse_receipt(content)

        doc = create_document(receipt=receipt, data=content)
        connector.add_document(doc)

        bot.send_message(
            message.chat.id,
            i18n.t(
                "bot.receipt_result",
                seller=receipt["seller"],
                total_sum=receipt["sum"],
                date=receipt["date"],
            ),
        )

        for msg in format_messages(receipt, clf):
            bot.send_message(message.chat.id, msg)

    except Exception as error:
        bot.send_message(message.chat.id, i18n.t("bot.general_error"))
        logger.error(f"Failed to process the receipt: {error}")


if __name__ == "__main__":

    bot = TeleBot(
        settings.API_TOKEN,
        num_threads=settings.NUM_THREADS,
    )

    connector = Connector(
        uri=settings.DB_URI,
        name=settings.DB_NAME,
        collection=settings.DB_COLLECTION,
    )

    clf = GoodsClassifier().load()

    @bot.message_handler(commands=["start", "help"])
    def handle_start_command(message: types.Message):
        logger.debug(f"Got message: {message}")
        bot.reply_to(
            message,
            i18n.t("bot.welcome"),
        )

    @bot.message_handler(content_types=["document"])
    def handle_receipt(message: types.Message):
        logger.debug(f"Got message: {message}")
        bot.reply_to(
            message,
            i18n.t("bot.receipt_confirmation"),
        )
        process_receipt(bot, message, connector, clf)

    bot.infinity_polling()
