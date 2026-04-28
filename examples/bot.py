import asyncio
import logging
import sys

from aiogram import Dispatcher, html, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from aiogram_listview.listview import ListView
from aiogram_listview.listview_aiogram import print_list, router

from aiogram_listview.listview_storage import MemoryListViewStorage
from aiogram_listview.listview_middleware import ListViewMiddleware

dp = Dispatcher()

storage = MemoryListViewStorage()
dp.update.middleware(ListViewMiddleware(storage))

dp.include_router(router)


async def handle_item_selection(callback: CallbackQuery, item: any, index: int):
    await callback.answer(f"You picked {item}!")
    await callback.message.answer(f"✨ Custom selection logic: Item {item} at index {index}")


def item_formatter(idx, value):
    return f"🔹 {html.bold(f'Item #{idx}')}: {value}"


@dp.message(CommandStart())
async def command_start_handler(
    message: Message, 
    bot: Bot,
    listview_storage: MemoryListViewStorage
) -> None:
    data = ["Apple", "Banana", "Cherry", "Date", "Elderberry", "Fig", "Grape", "Honeydew"]
    
    lv = ListView(
        data, 
        id="fruit_list", 
        page_size=3, 
        is_show_page=True, 
        start_text="🍎 Choose your favorite fruit:\n\n",
        formatter=item_formatter
    )
    
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}! Here is your list:")
    
    await print_list(
        chat_id=message.chat.id, 
        lv=lv, 
        storage=listview_storage, 
        bot=bot, 
        replacement=False
    )


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())