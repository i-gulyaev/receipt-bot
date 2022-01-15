import json
import logging
from typing import List

import i18n
from telebot import TeleBot
from telebot import logger as tb_logger
from telebot import types

from app.schemas import Receipt, ReceiptItem
from app.settings import settings
from app.utils import parse_receipt

logger = tb_logger
tb_logger.setLevel(logging.DEBUG)

i18n.load_path.append(settings.I18N_PATH)
i18n.set("locale", "ru")
i18n.set("fallback", "en")

MAX_MESSAGE_SIZE = 4096


def stringify_item(date, item: ReceiptItem) -> str:
    name = item.name.replace(";", ".")
    return f"{date};unknown;{name};{item.total_sum}"


def format_messages(
    receipt: Receipt,
    message_size: int = MAX_MESSAGE_SIZE,
) -> List[str]:
    result = []
    date = receipt.date.strftime("%Y-%m-%d")

    message = ""

    items = [stringify_item(date, item) for item in receipt.items]

    for item in items:
        if (len(message) + len(item) + 1) > message_size:
            result.append(message)
            message = ""
        message += item + "\n"

    if message:
        result.append(message)

    return result


def process_receipt(bot: TeleBot, message: types.Message):
    assert message.document
    try:
        file_info = bot.get_file(message.document.file_id)
        content = bot.download_file(file_info.file_path)

        content = json.loads(content)
        logger.debug(f"Get file={file_info}, content={content}")
        receipt = parse_receipt(content)

        bot.send_message(
            message.chat.id,
            i18n.t(
                "bot.receipt_result",
                seller=receipt.seller,
                total_sum=receipt.total_sum,
                date=receipt.date,
            ),
        )

        for msg in format_messages(receipt):
            bot.send_message(message.chat.id, msg)

    except Exception as error:
        bot.send_message(message.chat.id, i18n.t("bot.general_error"))
        logger.error(f"Failed to process the receipt: {error}")


if __name__ == "__main__":

    bot = TeleBot(
        settings.API_TOKEN,
        num_threads=settings.NUM_THREADS,
    )

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
        process_receipt(bot, message)

    bot.infinity_polling()
