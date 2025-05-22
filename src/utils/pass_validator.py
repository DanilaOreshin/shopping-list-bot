import hashlib

from src.config.bot_settings import settings


def is_valid_pass(password: str):
    return hashlib.md5(password.encode()).hexdigest() == settings.BOT_MASTER_PASSWORD
