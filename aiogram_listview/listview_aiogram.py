from typing import Optional, Callable, Awaitable, Any, Union
import logging

from aiogram import Router, Bot, html
from aiogram.types import InlineKeyboardButton, CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from aiogram_listview.listview_storage import ListViewStorage
from aiogram_listview.listview import ListView
from aiogram_listview.listview_controller import get_bot, get_storage

logger = logging.getLogger(__name__)
router = Router()

# Registry for custom selection handlers
# Key: list_id, Value: handler function
_selection_handlers: dict[str, Callable[[CallbackQuery, Any, int], Awaitable[None]]] = {}


def register_selection_handler(list_id: str, handler: Callable[[CallbackQuery, Any, int], Awaitable[None]]):
    """Registers a custom handler for element selection in a specific list."""
    _selection_handlers[list_id] = handler


class ListViewCallback(CallbackData, prefix='listview'):
    id: str
    move: int


class ListViewSelectElementCallback(CallbackData, prefix='listview_select_el'):
    id: str
    index: int


@router.callback_query(ListViewCallback.filter())
async def list_view_move_callback_handler(callback: CallbackQuery, callback_data: ListViewCallback) -> None:
    bot = get_bot()
    storage = get_storage()

    lv = storage.get_listview(callback.from_user.id, callback_data.id)
    if not lv:
        await callback.answer("This list has expired or is no longer available.", show_alert=True)
        return

    if callback_data.move == 1:
        await callback.answer("Next page")
        lv.next()
        await print_list(callback.message.chat.id, lv, storage, True, bot)
    elif callback_data.move == -1:
        await callback.answer("Previous page")
        lv.previous()
        await print_list(callback.message.chat.id, lv, storage, True, bot)
    else:
        await callback.answer()


@router.callback_query(ListViewSelectElementCallback.filter())
async def list_view_select_element_callback_handler(callback: CallbackQuery, callback_data: ListViewSelectElementCallback) -> None:
    storage = get_storage()
    lv = storage.get_listview(callback.from_user.id, callback_data.id)
    
    if not lv:
        await callback.answer("This list has expired.", show_alert=True)
        return

    if callback_data.index < 0 or callback_data.index >= len(lv._data):
        await callback.answer("Invalid selection.", show_alert=True)
        return

    selected_item = lv._data[callback_data.index]
    
    # Check if there is a custom handler for this list_id
    handler = _selection_handlers.get(lv._id)
    if handler:
        await handler(callback, selected_item, callback_data.index)
    else:
        # Default behavior
        await callback.answer(f"Selected: {str(selected_item)[:50]}")
        await callback.message.answer(f"You selected item #{callback_data.index + 1}: {selected_item}")


async def print_list(
    chat_id: int, 
    lv: ListView, 
    storage: ListViewStorage, 
    replacement: bool = False, 
    bot: Optional[Bot] = None
) -> Union[Message, bool]:
    if not bot:
        bot = get_bot()
    
    text = lv.get_display_text()

    data_list, start_index, end_index = lv.slice_data()
    buttons = []
    
    for i, element in enumerate(data_list):
        current_idx = start_index + i
        if lv._is_show_content_instead_of_indexes:
            btn_text = str(element)
        else:
            btn_text = str(current_idx + 1)
            
        buttons.append(
            InlineKeyboardButton(
                text=btn_text, 
                callback_data=ListViewSelectElementCallback(id=lv._id, index=current_idx).pack()
            )
        )
    
    builder = InlineKeyboardBuilder()
    if buttons:
        builder.add(*buttons)
        builder.adjust(2)

    nav_builder = InlineKeyboardBuilder()
    if lv.has_more_than_one_page():
        nav_builder.row(
            InlineKeyboardButton(text="⬅️ Previous", callback_data=ListViewCallback(id=lv._id, move=-1).pack()),
            InlineKeyboardButton(text=f"{lv._current_page}/{lv.get_max_page()}", callback_data="ignore"),
            InlineKeyboardButton(text="Next ➡️", callback_data=ListViewCallback(id=lv._id, move=1).pack())
        )

    builder.attach(nav_builder)
    markup = builder.as_markup()

    try:
        if replacement:
            message_id = storage.get_listview_message(chat_id, lv._id)
            if message_id:
                response = await bot.edit_message_text(
                    text=text, 
                    chat_id=chat_id, 
                    message_id=message_id, 
                    reply_markup=markup,
                    parse_mode="HTML"
                )
            else:
                response = await bot.send_message(text=text, chat_id=chat_id, reply_markup=markup, parse_mode="HTML")
        else:
            response = await bot.send_message(text=text, chat_id=chat_id, reply_markup=markup, parse_mode="HTML")
            
        storage.save_listview(chat_id, lv)
        storage.save_listview_message(chat_id, lv._id, response.message_id)
        return response
    except Exception as e:
        logger.error(f"Error printing list: {e}")
        # If editing failed, try sending a new message
        if replacement:
            response = await bot.send_message(text=text, chat_id=chat_id, reply_markup=markup, parse_mode="HTML")
            storage.save_listview(chat_id, lv)
            storage.save_listview_message(chat_id, lv._id, response.message_id)
            return response
        return False
