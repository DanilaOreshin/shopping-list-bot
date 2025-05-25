from aiogram.types import Message
from sqlalchemy import text, TextClause
from sqlalchemy.ext.asyncio import create_async_engine

from src.config.bot_settings import settings

async_engine = create_async_engine(url=settings.DATABASE_URL,
                                   echo=False,
                                   pool_size=10,
                                   max_overflow=5)


async def sql_modify(statement: TextClause):
    async with async_engine.connect() as conn:
        await conn.execute(statement)
        await conn.commit()


async def sql_select(statement: TextClause):
    async with async_engine.connect() as conn:
        res = await conn.execute(statement)
        return res.all()


def check_exists_user_query(user_id: int) -> TextClause:
    query = '''SELECT EXISTS (SELECT * FROM db_shopping_list.tuser tu WHERE tu.user_id = :user_id) AS res;'''
    return text(query).bindparams(user_id=user_id)


def insert_user_query(user_id: int, first_name: str, last_name: str) -> TextClause:
    query = '''INSERT INTO db_shopping_list.tuser(user_id, first_name, last_name) 
                VALUES (:user_id, :first_name, :last_name);'''
    return text(query).bindparams(user_id=user_id,
                                  first_name=first_name,
                                  last_name=last_name)


def check_exists_list_query(user_id: int, list_title: str) -> TextClause:
    query = '''SELECT EXISTS (SELECT *
                FROM db_shopping_list.tshopping_list tsl
                WHERE tsl.title = :list_title
                AND tsl.tuser_id IN (
                    SELECT tu.id
                    FROM db_shopping_list.tuser tu
                    WHERE tu.user_id = :user_id)
                ) AS res;'''
    return text(query).bindparams(user_id=user_id,
                                  list_title=list_title)


def insert_shopping_list_query(user_id: int, list_title: str) -> TextClause:
    query = '''INSERT INTO db_shopping_list.tshopping_list(title, tuser_id)
                VALUES (:list_title,(SELECT id FROM db_shopping_list.tuser WHERE user_id = :user_id));'''
    return text(query).bindparams(user_id=user_id,
                                  list_title=list_title)


def update_shopping_list_query(list_id: int, list_title: str) -> TextClause:
    query = '''UPDATE db_shopping_list.tshopping_list SET title = :list_title WHERE id = :list_id;'''
    return text(query).bindparams(list_id=list_id,
                                  list_title=list_title)


def delete_shopping_list_query(list_id: int) -> TextClause:
    query = '''DELETE FROM db_shopping_list.tshopping_list WHERE id = :list_id;'''
    return text(query).bindparams(list_id=list_id)


def select_lists_by_user_query(user_id: int) -> TextClause:
    query = '''SELECT tsl.id, tsl.title
                FROM db_shopping_list.tshopping_list tsl
                WHERE tsl.tuser_id IN (SELECT tu.id
                                        FROM db_shopping_list.tuser tu
                                        WHERE tu.user_id = :user_id)
                ORDER BY tsl.title ASC;'''
    return text(query).bindparams(user_id=user_id)


def check_exists_product_query(list_id: int, item_title: str) -> TextClause:
    query = '''SELECT EXISTS (
                    SELECT * FROM db_shopping_list.tproduct tp
                    WHERE tp.tshopping_list_id = :list_id
                    AND tp.title = :item_title
                ) AS res;'''
    return text(query).bindparams(list_id=list_id,
                                  item_title=item_title)


def insert_item_query(item_title: str, item_count: int, list_id: int) -> TextClause:
    query = '''INSERT INTO db_shopping_list.tproduct(title, count, tshopping_list_id)
                VALUES (:item_title, :item_count, :list_id);'''
    return text(query).bindparams(item_title=item_title,
                                  item_count=item_count,
                                  list_id=list_id)


def delete_item_query(item_id: int) -> TextClause:
    query = '''DELETE FROM db_shopping_list.tproduct WHERE id = :item_id;'''
    return text(query).bindparams(item_id=item_id)


def delete_all_items_by_list_query(list_id: int) -> TextClause:
    query = '''DELETE FROM db_shopping_list.tproduct WHERE tshopping_list_id = :list_id;'''
    return text(query).bindparams(list_id=list_id)


def check_item_query(item_id: int, is_checked: bool) -> TextClause:
    query = '''UPDATE db_shopping_list.tproduct SET is_checked = :is_checked WHERE id = :item_id;'''
    return text(query).bindparams(item_id=item_id,
                                  is_checked=is_checked)


def select_items_by_list_query(list_id: int) -> TextClause:
    query = '''SELECT tp.id, tp.title, tp.count, tp.is_checked
                FROM db_shopping_list.tproduct tp
                WHERE tp.tshopping_list_id = :list_id
                ORDER BY tp.is_checked ASC;'''
    return text(query).bindparams(list_id=list_id)


def select_full_list_info_query(list_id: int) -> TextClause:
    query = '''SELECT tsl.title, tp.id, tp.title, tp.count, tp.is_checked
                FROM db_shopping_list.tshopping_list tsl
                LEFT JOIN db_shopping_list.tproduct tp ON
                tsl.id = tp.tshopping_list_id
                WHERE tsl.id = :list_id
                ORDER BY tp.title ASC;'''
    return text(query).bindparams(list_id=list_id)


def insert_message_query(message_id: int, chat_id: int) -> TextClause:
    query = '''INSERT INTO db_shopping_list.tmessage (message_id, chat_id) VALUES (:message_id, :chat_id);'''
    return text(query).bindparams(message_id=message_id,
                                  chat_id=chat_id)


def select_messages_query(chat_id: int) -> TextClause:
    query = '''SELECT tm.message_id FROM db_shopping_list.tmessage tm WHERE tm.chat_id = :chat_id;'''
    return text(query).bindparams(chat_id=chat_id)


def delete_messages_by_chat_id_query(chat_id: int) -> TextClause:
    query = '''DELETE FROM db_shopping_list.tmessage WHERE chat_id = :chat_id;'''
    return text(query).bindparams(chat_id=chat_id)


def select_old_messages_query(interval: str) -> TextClause:
    query = f'''SELECT tm.chat_id, tm.message_id FROM db_shopping_list.tmessage tm 
                WHERE tm.create_date < now() - INTERVAL '{interval}';'''
    return text(query)


def delete_messages_by_message_ids_query(message_ids: list) -> TextClause:
    query = '''DELETE FROM db_shopping_list.tmessage WHERE message_id = ANY(:message_ids);'''
    return text(query).bindparams(message_ids=message_ids)


def assign_list_query(list_id: int, user_id: int) -> TextClause:
    query = '''UPDATE db_shopping_list.tshopping_list
                SET tuser_id = (SELECT tu.id FROM db_shopping_list.tuser tu WHERE tu.user_id = :user_id)
                WHERE id = :list_id;'''
    return text(query).bindparams(list_id=list_id,
                                  user_id=user_id)


async def save_message(message: Message):
    await sql_modify(insert_message_query(message.message_id, message.chat.id))
