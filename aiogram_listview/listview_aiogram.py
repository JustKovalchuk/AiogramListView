from typing import Optional

from aiogram import Router
from aiogram.types import InlineKeyboardButton
from aiogram import Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData, CallbackQuery

from aiogram_listview.listview_storage import ListViewStorage
from aiogram_listview.listview import ListView
from aiogram_listview.listview_controller import get_bot, get_storage

router = Router()


class ListViewCallback(CallbackData, prefix='listview'):
    id: Optional[str] = None
    move: Optional[int] = None
    # current_page: Optional[int] = None
    #
    # index: Optional[int] = None
    # last_page: Optional[int] = None
    # extra_act: Optional[str] = None
    # extra_index: Optional[int] = None


class ListViewSelectElementCallback(CallbackData, prefix='listview_select_el'):
    id: Optional[str] = None
    index: Optional[int] = None


@router.callback_query(ListViewCallback.filter())
async def list_view_move_callback_handler(callback: CallbackQuery, callback_data: ListViewCallback) -> None:
    bot = get_bot()
    storage = get_storage()

    lv = storage.get_listview(callback.from_user.id)
    if callback_data.move >= 1:
        await callback.answer("Next page!")
        lv.next()
        await print_list(callback.from_user.id, lv, storage, True, bot)
    elif callback_data.move <= -1:
        await callback.answer("Previous page!")
        lv.previous()
        await print_list(callback.from_user.id, lv, storage, True, bot)
    else:
        await callback.answer("Error page!")


@router.callback_query(ListViewSelectElementCallback.filter())
async def list_view_select_element_callback_handler(callback: CallbackQuery, callback_data: ListViewSelectElementCallback) -> None:
    storage = get_storage()
    lv = storage.get_listview(callback.from_user.id)
    await callback.answer("Selected element!")
    await callback.message.answer(f"Selected element: {lv._data[callback_data.index]}\nContent: {lv._data[callback_data.index]}")


async def print_list(chat_id, lv: ListView, storage: ListViewStorage, replacement: bool, bot: Bot) -> None:
    text = lv.get_display_text()

    data_list, start_index, end_index = lv.slice_data()
    buttons = []
    for element in data_list:
        start_index += 1
        if lv._is_show_content_instead_of_indexes:
            btn_text = str(element)
        else:
            btn_text = str(start_index)
        buttons.append(InlineKeyboardButton(text=btn_text, callback_data=ListViewSelectElementCallback(id=lv._id, index=start_index-1).pack()))
    builder = InlineKeyboardBuilder([buttons]).adjust(2, 2)

    append_builder = InlineKeyboardBuilder()
    if lv.has_more_than_one_page():
        append_builder.add(InlineKeyboardButton(text="Previous", callback_data=ListViewCallback(id=lv._id, move=-1).pack()))
        if lv._is_show_page:
             append_builder.add(InlineKeyboardButton(text=f"{lv._current_page}/{lv.get_max_page()}",
                                              callback_data=ListViewCallback(id=lv._id, move=0).pack()))
        append_builder.add(InlineKeyboardButton(text="Next", callback_data=ListViewCallback(id=lv._id, move=1).pack()))

    markup = builder.attach(append_builder).as_markup()

    # for html like bots
    text = text.replace("<", "")
    text = text.replace(">", "")

    if replacement:
        message_id = storage.get_listview_message(chat_id)
        response = await bot.edit_message_text(text=text, chat_id=chat_id, message_id=message_id, reply_markup=markup)
    else:
        response = await bot.send_message(text=text, chat_id=chat_id, reply_markup=markup)

    storage.save_listview(chat_id, lv)
    storage.save_listview_message(chat_id, response.message_id)
