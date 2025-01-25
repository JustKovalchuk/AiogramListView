from os import getenv
from dotenv import load_dotenv

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from aiogram_listview import listview_storage
from aiogram_listview.listview_controller import set_bot, get_bot, set_storage, get_storage


load_dotenv()
TOKEN = getenv("BOT_TOKEN")
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

storage = listview_storage.ListViewStorage()

set_bot(bot)
set_storage(storage)
