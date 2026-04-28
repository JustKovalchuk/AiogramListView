from aiogram import Bot
from aiogram_listview.listview_storage import ListViewStorage

bot: Bot = None
storage: ListViewStorage = None

def get_bot() -> Bot:
    return bot

def set_bot(bot_: Bot) -> None:
    global bot
    bot = bot_

def get_storage() -> ListViewStorage:
    return storage

def set_storage(storage_: ListViewStorage) -> None:
    global storage
    storage = storage_
