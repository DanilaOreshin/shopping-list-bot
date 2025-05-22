from aiogram.types import Message

from src.config import messages as m
from src.filters.check_user import is_registered
from src.keyboards import keyboard_builder as kb
from src.keyboards.button import Button
from src.utils import db_manager as db
from src.utils import message_sender as ms


# handlers
async def start_command_handler(message: Message):
    await db.save_message(message)
    if not await is_registered(message.from_user.id):
        text = m.start_registration_text
        builder = kb.get_inline_keyboard([Button(text='Регистрация', callback_data='register')])
        await ms.send_message_answer_with_buttons(message, text, builder.as_markup())
    else:
        text = m.welcome_text
        builder = kb.get_reply_keyboard([Button(text='Мои списки'), Button(text='Создать список')])
        await message.answer(text, reply_markup=builder.as_markup(resize_keyboard=True))


async def about_command_handler(message: Message):
    await db.save_message(message)
    text = m.about_text
    await ms.send_message_answer(message, text)
