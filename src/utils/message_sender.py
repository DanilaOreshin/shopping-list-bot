from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardMarkup

from src.utils import db_manager as db


async def send_call_answer(call: CallbackQuery, text: str):
    sent_message = await call.message.answer(text)
    await db.save_message(sent_message)
    await call.answer()


async def send_message_answer(message: Message, text: str):
    sent_message = await message.answer(text)
    await db.save_message(sent_message)


async def send_call_answer_with_buttons(call: CallbackQuery, text: str, markup: InlineKeyboardMarkup):
    sent_message = await call.message.answer(text, reply_markup=markup)
    await db.save_message(sent_message)
    await call.answer()


async def send_message_answer_with_buttons(message: Message, text: str, markup):
    sent_message = await message.answer(text, reply_markup=markup)
    await db.save_message(sent_message)
