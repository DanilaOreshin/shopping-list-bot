from datetime import datetime, timedelta

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.config import messages as m
from src.filters.check_user import is_registered
from src.handlers.command_handlers import start_command_handler
from src.keyboards import keyboard_builder as kb
from src.keyboards.button import Button
from src.utils import db_manager as db
from src.utils import functions as f
from src.utils import message_sender as ms
from src.utils.callback_entity_data import CallbackEntityData
from src.utils.pass_validator import is_valid_pass
from src.utils.states import ListStates, RegistrationStates


async def cancel_handler(call: CallbackQuery, state: FSMContext):
    text = m.cancel_action_text
    await state.clear()
    await ms.send_call_answer(call, text)


async def start_register_handler(call: CallbackQuery, state: FSMContext):
    text = m.send_pass_text
    await state.set_state(RegistrationStates.PASSWORD_TYPING)
    await ms.send_call_answer(call, text)


async def end_register_handler(message: Message, state: FSMContext, bot: Bot):
    await db.save_message(message)
    if is_valid_pass(message.text):
        # clear previous messages
        await f.clear_chat(bot, message.chat.id)
        # collect user data and save to db
        user_id = message.from_user.id
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        text = m.success_user_create_text
        await db.sql_modify(db.insert_user_query(user_id, first_name, last_name))
        # answer
        await state.clear()
        await ms.send_message_answer(message, text)
        await start_command_handler(message)
    else:
        # draw cancel button
        text = m.wrong_pass_text
        builder = kb.get_inline_keyboard([Button(text=m.cancel_button_text, callback_data='cancel_action')])
        await ms.send_message_answer_with_buttons(message, text, builder.as_markup())


async def start_create_list_handler(message: Message, state: FSMContext):
    await db.save_message(message)
    # answer
    text = m.send_list_name_text
    await state.set_state(ListStates.CREATE_LIST_NAMING)
    await ms.send_message_answer(message, text)


async def end_create_list_handler(message: Message, state: FSMContext, bot: Bot):
    await db.save_message(message)
    # clear previous messages
    await f.clear_chat(bot, message.chat.id)
    # check list exists
    user_id = message.from_user.id
    list_title = message.text
    if not (await db.sql_select(db.check_exists_list_query(user_id, list_title)))[0][0]:
        # save list to db
        await db.sql_modify(db.insert_shopping_list_query(user_id, list_title))
        # answer
        text = m.success_list_create_text.format(list_title)
        await state.clear()
        await ms.send_message_answer(message, text)
    else:
        # draw cancel button
        text = m.list_exists_text
        builder = kb.get_inline_keyboard([Button(text=m.cancel_button_text, callback_data='cancel_action')])
        await ms.send_message_answer_with_buttons(message, text, builder.as_markup())
    await f.get_my_lists_message(message)


async def start_update_list_handler(call: CallbackQuery, callback_data: CallbackEntityData, state: FSMContext):
    text = m.send_list_new_name_text
    # saving list_id to RAM
    await state.update_data(entity_id=callback_data.entity_id)
    await state.set_state(ListStates.UPDATE_LIST_NAMING)
    await ms.send_call_answer(call, text)


async def end_update_list_handler(message: Message, state: FSMContext, bot: Bot):
    await db.save_message(message)
    # clear previous messages
    await f.clear_chat(bot, message.chat.id)
    # check list exists
    entity_id = (await state.get_data())['entity_id']
    list_title = message.text
    if not (await db.sql_select(db.check_exists_list_query(message.from_user.id, list_title)))[0][0]:
        # update list into db
        await db.sql_modify(db.update_shopping_list_query(entity_id, list_title))
        text = m.success_list_update_text
        await state.clear()
        await ms.send_message_answer(message, text)
    else:
        # draw cancel button
        text = m.list_exists_text
        builder = kb.get_inline_keyboard([Button(text=m.cancel_button_text, callback_data='cancel_action')])
        await ms.send_message_answer_with_buttons(message, text, builder.as_markup())
    await f.get_list_preview_message(message=message, list_id=entity_id)


async def start_delete_list_handler(call: CallbackQuery, callback_data: CallbackEntityData, state: FSMContext):
    text = m.delete_list_confirm_text
    # saving list_id to RAM
    await state.update_data(entity_id=callback_data.entity_id)
    builder = kb.get_inline_keyboard([Button(text=m.yes_button_text, callback_data='confirm_delete_list'),
                                      Button(text=m.cancel_button_text, callback_data='cancel_action')])
    await ms.send_call_answer_with_buttons(call, text, builder.as_markup())


async def end_delete_list_handler(call: CallbackQuery, state: FSMContext, bot: Bot):
    # clear previous messages
    await f.clear_chat(bot, call.message.chat.id)
    # delete products and list from db
    entity_id = (await state.get_data())['entity_id']
    await db.sql_modify(db.delete_all_items_by_list_query(entity_id))
    await db.sql_modify(db.delete_shopping_list_query(entity_id))
    # answer
    text = m.success_list_delete_text
    await call.answer(text)
    await f.get_my_lists_call(call)


async def get_my_lists_handler(message: Message, bot: Bot):
    # clear previous messages
    await f.clear_chat(bot, message.chat.id)
    # draw list of lists :)
    await f.get_my_lists_message(message)


async def get_list_preview_handler(call: CallbackQuery, callback_data: CallbackEntityData, bot: Bot):
    # clear previous messages
    await f.clear_chat(bot, call.message.chat.id)
    # draw list preview
    await f.get_list_preview_call(call=call, list_id=callback_data.entity_id)


async def get_list_items_handler(call: CallbackQuery, callback_data: CallbackEntityData):
    # select list's products from db
    all_products = await db.sql_select(db.select_items_by_list_query(callback_data.entity_id))
    if not all_products:
        text = m.list_is_empty_text
        await ms.send_call_answer(call, text)
        return
    else:
        number = 1
        text = m.show_list_items_prefix_text
        await ms.send_call_answer(call, text)
        for product_item in all_products:
            # collect data and configure item card message and buttons
            product_id = product_item[0]
            product_title = product_item[1]
            product_count = product_item[2]
            product_check = product_item[3]
            check_button_text = m.check_item_text if product_check is True else m.uncheck_item_text
            product_count_str = f' - {product_count} шт.' if product_count else ''
            text = f'{number}. {product_title}{product_count_str}\n'
            builder = kb.get_inline_keyboard([Button(text=check_button_text,
                                                     callback_data=CallbackEntityData(action='check_product',
                                                                                      entity_id=product_id)),
                                              Button(text=m.delete_button_text,
                                                     callback_data=CallbackEntityData(action='delete_product',
                                                                                      entity_id=product_id))])
            await ms.send_call_answer_with_buttons(call, text, builder.as_markup())
            number += 1


async def start_add_items_handler(call: CallbackQuery, callback_data: CallbackEntityData, state: FSMContext):
    text = m.send_items_text
    # saving list_id to RAM
    await state.update_data(entity_id=callback_data.entity_id)
    await state.set_state(ListStates.ADD_ITEMS_TO_LIST)
    await ms.send_call_answer(call, text)


async def end_add_items_handler(message: Message, state: FSMContext, bot: Bot):
    await db.save_message(message)
    # clear previous messages
    await f.clear_chat(bot, message.chat.id)
    # parsing message and draw cancel button if error
    parsed_array = f.parse_product_items(message.text)
    if not parsed_array:
        text = m.cant_parse_items_data_text
        builder = kb.get_inline_keyboard([Button(text=m.cancel_button_text, callback_data='cancel_action')])
        await ms.send_message_answer_with_buttons(message, text, builder.as_markup())
        return
    # collect data and saving items to db
    entity_id = (await state.get_data())['entity_id']
    partly_list = ''
    is_anyone_add = False
    for item in parsed_array:
        if not (await db.sql_select(db.check_exists_product_query(entity_id, item[0])))[0][0]:
            await db.sql_modify(db.insert_item_query(item[0], item[1], entity_id))
            is_anyone_add = True
        else:
            partly_list += f'{item[0]}\n'
    # create outer message text
    if not is_anyone_add:
        text = m.no_one_item_insert_text
    elif partly_list != '':
        text = m.partly_item_insert_text + partly_list
    else:
        text = m.all_item_insert_text
    # send response and redraw list preview
    await state.clear()
    await ms.send_message_answer(message, text)
    await f.get_list_preview_message(message=message, list_id=entity_id)


async def delete_item_handler(call: CallbackQuery, callback_data: CallbackEntityData):
    text = m.success_item_delete_text
    # delete item from db
    await db.sql_modify(db.delete_item_query(callback_data.entity_id))
    await call.answer(text)
    await call.message.delete()


async def check_item_handler(call: CallbackQuery, callback_data: CallbackEntityData):
    # update item flag into db
    previous_button_text = call.message.reply_markup.inline_keyboard[0][0].text
    if previous_button_text == m.check_item_text:
        next_button_text = m.uncheck_item_text
        await db.sql_modify(db.check_item_query(callback_data.entity_id, True))
    else:
        next_button_text = m.check_item_text
        await db.sql_modify(db.check_item_query(callback_data.entity_id, False))
    # redraw buttons
    builder = kb.get_inline_keyboard([Button(text=next_button_text,
                                             callback_data=CallbackEntityData(action='check_product',
                                                                              entity_id=callback_data.entity_id)),
                                      Button(text=m.delete_button_text,
                                             callback_data=CallbackEntityData(action='delete_product',
                                                                              entity_id=callback_data.entity_id))])
    await call.message.edit_text(text=call.message.text, reply_markup=builder.as_markup())
    await call.answer()


async def start_assign_list_handler(call: CallbackQuery, callback_data: CallbackEntityData, state: FSMContext):
    text = m.assign_list_confirm_text
    # saving list_id to RAM
    await state.update_data(entity_id=callback_data.entity_id)
    builder = kb.get_inline_keyboard([Button(text=m.yes_button_text, callback_data='confirm_assign_list'),
                                      Button(text=m.cancel_button_text, callback_data='cancel_action')])
    await ms.send_call_answer_with_buttons(call, text, builder.as_markup())


async def send_contact_assign_list_handler(call: CallbackQuery, state: FSMContext):
    text = m.send_contact_text
    await state.set_state(ListStates.ASSIGN_LIST)
    builder = kb.get_inline_keyboard([Button(text=m.cancel_button_text, callback_data='cancel_action')])
    await ms.send_call_answer_with_buttons(call, text, builder.as_markup())


async def end_assign_list_handler(message: Message, state: FSMContext, bot: Bot, apscheduler: AsyncIOScheduler):  #
    await db.save_message(message)
    contact_user_id = message.contact.user_id
    if not contact_user_id or not await is_registered(contact_user_id):
        text = m.wrong_contact_text
        builder = kb.get_inline_keyboard([Button(text=m.cancel_button_text, callback_data='cancel_action')])
        await ms.send_message_answer_with_buttons(message, text, builder.as_markup())
        return
    # assign list
    entity_id = (await state.get_data())['entity_id']
    await db.sql_modify(db.assign_list_query(entity_id, contact_user_id))
    # clear previous messages
    await f.clear_chat(bot, message.chat.id)
    text = m.list_assigned_successfully_text
    await state.clear()
    await ms.send_message_answer(message, text)
    await f.get_my_lists_message(message)
    apscheduler.add_job(scheduler_assign_list_notification, trigger='date',
                        run_date=datetime.now() + timedelta(seconds=10),
                        kwargs={'bot': bot, 'user_id': contact_user_id})


async def scheduler_assign_list_notification(bot: Bot, user_id: int):
    sent_message = await bot.send_message(user_id, 'Тебе назначен новый список!')
    await db.save_message(sent_message)
