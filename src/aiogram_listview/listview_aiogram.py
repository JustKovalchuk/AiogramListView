from typing import Optional, Callable, Awaitable, Any, Union
import logging
from aiogram import Router, Bot
from aiogram.types import InlineKeyboardButton, CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from aiogram_listview.listview_storage import BaseListViewStorage
from aiogram_listview.listview import ListView

logger = logging.getLogger(__name__)
router = Router()

class ListViewCallback(CallbackData, prefix='listview'):
    id: str
    move: int

class ListViewSelectElementCallback(CallbackData, prefix='listview_select_el'):
    id: str
    index: int

@router.callback_query(ListViewCallback.filter())
async def list_view_move_callback_handler(
    callback: CallbackQuery, 
    callback_data: ListViewCallback, 
    bot: Bot, 
    listview_storage: BaseListViewStorage
) -> None:
    lv = await listview_storage.get_listview(callback.from_user.id, callback_data.id)
    if not lv:
        await callback.answer("This list has expired or is no longer available.", show_alert=True)
        return

    if callback_data.move == 1:
        lv.next()
    elif callback_data.move == -1:
        lv.previous()
        
    await callback.answer()
    await print_list(callback.message.chat.id, lv, listview_storage, bot, replacement=True)


async def print_list(
    chat_id: int, 
    lv: ListView, 
    storage: BaseListViewStorage, 
    bot: Bot,
    replacement: bool = False
) -> Union[Message, bool]:
    
    text = lv.get_display_text()
    data_list, start_index, end_index = lv.slice_data()
    buttons = []
    
    for i, element in enumerate(data_list):
        current_idx = start_index + i
        
        if lv.button_builder:
            btn = lv.button_builder(element, current_idx, lv.id)
            buttons.append(btn)
        else:
            btn_text = str(current_idx + 1)
            buttons.append(
                InlineKeyboardButton(
                    text=btn_text, 
                    callback_data=ListViewSelectElementCallback(id=lv.id, index=current_idx).pack()
                )
            )
    
    builder = InlineKeyboardBuilder()
    if buttons:
        builder.add(*buttons)
        builder.adjust(2)

    nav_builder = InlineKeyboardBuilder()
    if lv.has_more_than_one_page():
        nav_builder.row(
            InlineKeyboardButton(text="⬅️ Previous", callback_data=ListViewCallback(id=lv.id, move=-1).pack()),
            InlineKeyboardButton(text=f"{lv.current_page}/{lv.get_max_page()}", callback_data="ignore"),
            InlineKeyboardButton(text="Next ➡️", callback_data=ListViewCallback(id=lv.id, move=1).pack())
        )

    builder.attach(nav_builder)
    markup = builder.as_markup()

    try:
        if replacement:
            message_id = await storage.get_listview_message(chat_id, lv.id)
            if message_id:
                response = await bot.edit_message_text(
                    text=text, 
                    chat_id=chat_id, 
                    message_id=message_id, 
                    reply_markup=markup
                )
            else:
                response = await bot.send_message(text=text, chat_id=chat_id, reply_markup=markup)
        else:
            response = await bot.send_message(text=text, chat_id=chat_id, reply_markup=markup)
            
        await storage.save_listview(chat_id, lv)
        await storage.save_listview_message(chat_id, lv.id, response.message_id)
        return response
    except Exception as e:
        logger.error(f"Error printing list: {e}")
        return False
