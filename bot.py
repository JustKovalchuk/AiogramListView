import asyncio
import logging
import sys

from aiogram import Dispatcher, html
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from aiogram_listview.listview import ListView
from aiogram_listview.listview_aiogram import print_list, router, register_selection_handler
from aiogram_listview.listview_controller import get_storage

from bot_utils import bot

dp = Dispatcher()
dp.include_router(router)


async def handle_item_selection(callback: CallbackQuery, item: any, index: int):
    await callback.answer(f"You picked {item}!")
    await callback.message.answer(f"✨ Custom selection logic: Item {item} at index {index}")


# Custom formatter for list items
def item_formatter(idx, value):
    return f"🔹 {html.bold(f'Item #{idx}')}: {value}"


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    storage = get_storage()

    data = ["Apple", "Banana", "Cherry", "Date", "Elderberry", "Fig", "Grape", "Honeydew"]
    
    # Create ListView with custom id and settings
    lv = ListView(
        data, 
        id="fruit_list", 
        page_size=3, 
        is_show_page=True, 
        is_show_content_instead_of_indexes=True,
        start_text="🍎 Choose your favorite fruit:\n\n",
        formatter=item_formatter
    )
    
    # Register custom behavior for this list
    register_selection_handler("fruit_list", handle_item_selection)
    
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}! Here is your list:")
    await print_list(message.chat.id, lv, storage, replacement=False, bot=bot)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())