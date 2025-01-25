import asyncio
import logging
import sys

from aiogram import Dispatcher, html
from aiogram.filters import CommandStart
from aiogram.types import Message

from aiogram_listview.listview import ListView
from aiogram_listview.listview_aiogram import print_list, router
from aiogram_listview.listview_controller import get_storage

from bot_utils import bot

dp = Dispatcher()
dp.include_router(router)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    storage = get_storage()

    data = [1,2,3,4,5,6,7,8,9,10,11,12]
    lv = ListView(data, id="test", page_size=5, is_show_page=False, is_show_content_instead_of_indexes=True)
    lv.my_init()
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
    await print_list(message.from_user.id, lv, storage, False, bot)


@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())