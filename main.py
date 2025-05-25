import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import src.handlers.basic_handlers as bh
import src.handlers.command_handlers as ch
import src.handlers.message_handlers as mh
from src.config.bot_settings import settings
from src.config.menu_config import set_commands
from src.filters.check_user import IsUnregisteredUser
from src.middlewares.middleware_scheduler import MiddlewareScheduler
from src.utils.callback_entity_data import CallbackEntityData
from src.utils.functions import clear_old_messages
from src.utils.states import ListStates, RegistrationStates


async def start_bot(bot: Bot):
    await set_commands(bot)


async def start():
    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher()

    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(clear_old_messages,
                      trigger='interval',
                      hours=settings.INTERVAL_CLEAR_MSG_HOURS,
                      kwargs={'bot': bot})

    scheduler.start()
    dp.update.middleware.register(MiddlewareScheduler(scheduler))

    # add /start and /about commands to menu
    dp.startup.register(start_bot)

    # command handlers
    dp.message.register(ch.start_command_handler, Command(commands=['start']))
    dp.message.register(ch.about_command_handler, Command(commands=['about']))

    dp.callback_query.register(mh.cancel_handler, F.data == 'cancel_action')
    dp.message.register(mh.end_register_handler, RegistrationStates.PASSWORD_TYPING)

    # valid user check
    dp.message.register(bh.wrong_user_handler, IsUnregisteredUser())

    # reply menu handlers
    dp.message.register(mh.get_my_lists_handler, F.text == 'Мои списки')
    dp.message.register(mh.start_create_list_handler, F.text == 'Создать список')

    # state handlers
    dp.message.register(mh.end_create_list_handler, ListStates.CREATE_LIST_NAMING)
    dp.message.register(mh.end_update_list_handler, ListStates.UPDATE_LIST_NAMING)
    dp.message.register(mh.end_add_items_handler, ListStates.ADD_ITEMS_TO_LIST)
    dp.message.register(mh.end_assign_list_handler, ListStates.ASSIGN_LIST)

    # callback handlers
    dp.callback_query.register(mh.start_register_handler, F.data == 'register')
    dp.callback_query.register(mh.start_update_list_handler, CallbackEntityData.filter(F.action == 'update_list'))
    dp.callback_query.register(mh.start_delete_list_handler, CallbackEntityData.filter(F.action == 'delete_list'))
    dp.callback_query.register(mh.end_delete_list_handler, F.data == 'confirm_delete_list')
    dp.callback_query.register(mh.get_list_preview_handler, CallbackEntityData.filter(F.action == 'watch_list_preview'))
    dp.callback_query.register(mh.get_list_items_handler,
                               CallbackEntityData.filter(F.action == 'watch_list_items'))
    dp.callback_query.register(mh.start_add_items_handler, CallbackEntityData.filter(F.action == 'add_items_to_list'))

    dp.callback_query.register(mh.check_item_handler, CallbackEntityData.filter(F.action == 'check_product'))
    dp.callback_query.register(mh.delete_item_handler, CallbackEntityData.filter(F.action == 'delete_product'))
    dp.callback_query.register(mh.start_assign_list_handler, CallbackEntityData.filter(F.action == 'assign_list'))
    dp.callback_query.register(mh.send_contact_assign_list_handler, F.data == 'confirm_assign_list')

    # default handlers
    dp.message.register(bh.default_handler)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
