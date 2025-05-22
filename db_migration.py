import asyncio

from sqlalchemy import text

import src.utils.db_manager as db

CREATE_TUSER = '''CREATE TABLE db_shopping_list.tuser (
    id bigserial NOT NULL,
    user_id int8 NOT NULL,
    first_name varchar(100) NULL,
    last_name varchar(100) NULL,
    create_date timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT pk_tuser_id PRIMARY KEY (id),
    CONSTRAINT un_tuser_user_id UNIQUE (user_id)
);'''

CREATE_TUSER_USER_ID_INDEX = '''CREATE INDEX idx_tuser_user_id ON db_shopping_list.tuser USING btree (user_id);'''

CREATE_TSHOPPING_LIST = '''CREATE TABLE db_shopping_list.tshopping_list (
    id bigserial NOT NULL,
    title varchar(255) NOT NULL,
    tuser_id int8 NOT NULL,
    create_date timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    update_date timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT pk_tshopping_list_id PRIMARY KEY (id),
    CONSTRAINT fk_tshopping_list_tuser_id FOREIGN KEY (tuser_id) REFERENCES db_shopping_list.tuser(id)
);'''

CREATE_TSHOPPING_LIST_TUSER_ID_INDEX = '''CREATE INDEX idx_tshopping_list_tuser_id ON db_shopping_list.tshopping_list 
                                                                                             USING btree (tuser_id);'''

CREATE_TSHOPPING_LIST_UNIQUE_INDEX = '''CREATE UNIQUE INDEX idx_un_tshopping_list_title_tuser_id ON 
                                                      db_shopping_list.tshopping_list USING btree (title, tuser_id);'''

CREATE_TPRODUCT = '''CREATE TABLE db_shopping_list.tproduct (
    id bigserial NOT NULL,
    title varchar(255) NOT NULL,
    count int8 NULL,
    tshopping_list_id int8 NOT NULL,
    is_checked bool DEFAULT false NOT NULL,
    create_date timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    update_date timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT pk_tproduct_id PRIMARY KEY (id),
    CONSTRAINT fk_tproduct_tshopping_list FOREIGN KEY (tshopping_list_id) REFERENCES db_shopping_list.tshopping_list(id)
);'''

CREATE_TPRODUCT_TSHOPPING_LIST_ID_INDEX = '''CREATE INDEX idx_tproduct_tshopping_list_id ON db_shopping_list.tproduct 
                                                                                    USING btree (tshopping_list_id);'''

CREATE_TPRODUCT_UNIQUE_INDEX = '''CREATE UNIQUE INDEX idx_un_tproduct_title_tshopping_list_id ON 
                                                   db_shopping_list.tproduct USING btree (title, tshopping_list_id);'''

CREATE_TMESSAGE = '''CREATE TABLE db_shopping_list.tmessage (
    id bigserial NOT NULL,
    message_id int8 NOT NULL,
    chat_id int8 NOT NULL,
    create_date timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT pk_tmessage_id PRIMARY KEY (id)
);'''

CREATE_TMESSAGE_CHAT_ID_INDEX = '''CREATE INDEX idx_tmessage_chat_id ON db_shopping_list.tmessage 
                                                                                      USING btree (chat_id);'''


async def migrate():
    await db.sql_modify(text(CREATE_TUSER))
    await db.sql_modify(text(CREATE_TUSER_USER_ID_INDEX))
    await db.sql_modify(text(CREATE_TSHOPPING_LIST))
    await db.sql_modify(text(CREATE_TSHOPPING_LIST_TUSER_ID_INDEX))
    await db.sql_modify(text(CREATE_TSHOPPING_LIST_UNIQUE_INDEX))
    await db.sql_modify(text(CREATE_TPRODUCT))
    await db.sql_modify(text(CREATE_TPRODUCT_TSHOPPING_LIST_ID_INDEX))
    await db.sql_modify(text(CREATE_TPRODUCT_UNIQUE_INDEX))
    await db.sql_modify(text(CREATE_TMESSAGE))
    await db.sql_modify(text(CREATE_TMESSAGE_CHAT_ID_INDEX))


asyncio.run(migrate())
