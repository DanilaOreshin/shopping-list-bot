from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.utils import db_manager as db


async def is_registered(user_id: int):
    res = await db.sql_select(db.check_exists_user_query(user_id))
    return res[0][0]


class IsUnregisteredUser(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id
        return not await is_registered(user_id)
