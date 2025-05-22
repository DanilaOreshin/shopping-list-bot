from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from src.keyboards.button import Button


def get_inline_keyboard(buttons: [Button]) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for b in buttons:
        builder.button(text=b.text, callback_data=b.callback_data)
    builder.adjust(2)
    return builder


def get_reply_keyboard(buttons: [Button]) -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    for b in buttons:
        builder.button(text=b.text, callback_data=b.callback_data)
    builder.adjust(2)
    return builder
