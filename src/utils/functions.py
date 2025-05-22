from aiogram import Bot
from aiogram import exceptions
from aiogram.types import Message, CallbackQuery

from src.config import messages as m
from src.keyboards import keyboard_builder as kb
from src.keyboards.button import Button
from src.utils import db_manager as db, message_sender as ms
from src.utils.callback_entity_data import CallbackEntityData
from src.utils.logger import logger


async def clear_chat(bot: Bot, chat_id: int):
    # select array of message_id from db
    result = await db.sql_select(db.select_messages_query(chat_id))
    message_ids = []
    for row in result:
        message_ids.append(row[0])
    # delete messages from chat and db
    if message_ids:
        await bot.delete_messages(chat_id=chat_id, message_ids=message_ids)
        await db.sql_modify(db.delete_messages_by_chat_id_query(chat_id))


def parse_product_items(raw_text: str):
    rows_array = raw_text.strip('\n').split('\n')
    result_array = []
    for row in rows_array:
        item_data = row.split('-')
        if len(item_data) > 2 or len(item_data) < 1:
            return []
        if len(item_data) < 2:
            item_data.append(None)
        item_data[0] = item_data[0].strip() if item_data[0] else None
        try:
            item_data[1] = int(item_data[1].strip()) if item_data[1] else None
        except ValueError:
            return []
        result_array.append(item_data)
    return result_array


async def get_my_lists_message(message: Message):
    await db.save_message(message)
    all_lists = await db.sql_select(db.select_lists_by_user_query(message.from_user.id))
    if not all_lists:
        text = m.no_lists_text
        await ms.send_message_answer(message, text)
        return
    text = m.my_lists_text
    await ms.send_message_answer(message, text)
    list_number = 1
    for list_item in all_lists:
        list_id = list_item[0]
        list_title = list_item[1]
        text = f'{list_number}. {list_title}'
        builder = kb.get_inline_keyboard([Button(text=m.preview_list_button_text,
                                                 callback_data=CallbackEntityData(action='watch_list_preview',
                                                                                  entity_id=list_id))])
        await ms.send_message_answer_with_buttons(message, text, builder.as_markup())
        list_number += 1


async def get_my_lists_call(call: CallbackQuery):
    await db.save_message(call.message)
    all_lists = await db.sql_select(db.select_lists_by_user_query(call.from_user.id))
    if not all_lists:
        text = m.no_lists_text
        await ms.send_call_answer(call, text)
        return
    text = m.my_lists_text
    await ms.send_call_answer(call, text)
    list_number = 1
    for list_item in all_lists:
        list_id = list_item[0]
        list_title = list_item[1]
        text = f'{list_number}. {list_title}'
        builder = kb.get_inline_keyboard([Button(text=m.preview_list_button_text,
                                                 callback_data=CallbackEntityData(action='watch_list_preview',
                                                                                  entity_id=list_id))])
        await ms.send_call_answer_with_buttons(call, text, builder.as_markup())
        list_number += 1


async def configurate_list_preview(list_id):
    # select list info from db
    list_items = await db.sql_select(db.select_full_list_info_query(list_id))
    # create buttons
    buttons = [Button(text=m.add_items_button_text,
                      callback_data=CallbackEntityData(action='add_items_to_list', entity_id=list_id)),
               Button(text=m.update_button_text,
                      callback_data=CallbackEntityData(action='update_list', entity_id=list_id)),
               Button(text=m.delete_button_text,
                      callback_data=CallbackEntityData(action='delete_list', entity_id=list_id))]
    # configure message if products exists
    if list_items[0][1]:
        text = m.list_preview_text.format(list_items[0][0], len(list_items))
        buttons.insert(0, Button(text=m.watch_items_button_text,
                                 callback_data=CallbackEntityData(action='watch_list_items', entity_id=list_id)))
        buttons.insert(1, Button(text=m.assign_list_button_text,
                                 callback_data=CallbackEntityData(action='assign_list', entity_id=list_id)))
        builder = kb.get_inline_keyboard(buttons)
        builder.adjust(2, 1, 2)
        number = 1
        for item in list_items:
            product_check = item[4]
            if product_check == 1:
                product_check_icon = m.check_icon
            else:
                product_check_icon = m.uncheck_icon
            text += f'{number}. {product_check_icon} {item[2]}'
            if item[3] is not None:
                product_count = f' - {item[3]} шт.\n'
            else:
                product_count = f'\n'
            text += product_count
            number += 1
    # configure message if products not exists
    else:
        text = m.list_preview_text.format(list_items[0][0], 0) + m.list_is_empty_text
        builder = kb.get_inline_keyboard(buttons)
        builder.adjust(1, 2)
    return builder, text


async def get_list_preview_call(call: CallbackQuery, list_id: int):
    builder, text = await configurate_list_preview(list_id)
    await ms.send_call_answer_with_buttons(call, text, builder.as_markup())


async def get_list_preview_message(message: Message, list_id: int):
    builder, text = await configurate_list_preview(list_id)
    await ms.send_message_answer_with_buttons(message, text, builder.as_markup())


async def clear_old_messages(bot: Bot):
    logger.info(f'search old messages')
    result = await db.sql_select(db.select_old_messages_query())
    if not result:
        logger.info(f'old messages not found')
        return
    message_ids = ''
    for row in result:
        chat_id = int(row[0])
        message_id = int(row[1])
        try:
            await bot.delete_message(chat_id=chat_id, message_id=message_id)
            logger.info(f'old message message_id was deleted from tg')
        except exceptions.TelegramBadRequest as ex:
            logger.error(f'chat_id = {chat_id}, message_id = {message_id}: {ex}')
        message_ids += str(row[1]) + ','
    message_ids = message_ids[:-1]
    await db.sql_modify(db.delete_messages_by_message_ids_query(message_ids))
    logger.info(f'old messages ({message_ids}) was deleted from db')
