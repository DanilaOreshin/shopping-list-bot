from aiogram.types import Message

from src.config import messages as m
from src.utils import db_manager as db
from src.utils import message_sender as ms


# handlers
async def default_handler(message: Message):
    await db.save_message(message)
    text = m.default_text
    await ms.send_message_answer(message, text)


async def wrong_user_handler(message: Message):
    await db.save_message(message)
    text = m.not_registered_text
    await ms.send_message_answer(message, text)
