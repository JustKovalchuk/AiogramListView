import math
from enum import Enum
from typing import Optional

from aiogram.types import Message
from aiogram import Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder
from aiogram.filters.callback_data import CallbackData, CallbackQuery


class ListViewCallback(CallbackData, prefix='listview'):
    id: Optional[str] = None
    current_page: Optional[int] = None

    move: Optional[str] = None
    index: Optional[int] = None
    last_page: Optional[int] = None
    extra_act: Optional[str] = None
    extra_index: Optional[int] = None

active_listviews = dict()
active_listview_messages = dict()


class ListType(Enum):
    ACTIVE_REQUESTS = "ACTIVE_REQUESTS"
    VERIFIED_USERS = "VERIFIED_USERS"
    AUTO_ANALYZE_PAIRS = "AUTO_ANALYZE_PAIRS"


class ListView:
    def __init__(self, data_list: list, id: str, page_size: int = 10, current_page: int = 1,
                 start_text="Data list:\n", end_text="", empty_data_text="No data found!"):
        self.id = id
        self.data = data_list
        self.page_size = page_size

        self.current_page = current_page

        self.start_text = start_text
        self.end_text = end_text
        self.empty_data_text = empty_data_text

    def __str__(self):
        return f"""Data: {self.data}\n
                   Current page: {self.current_page}\n
                   """

    def my_init(self):
        data_per_page = self.slice_data()

        builder = InlineKeyboardBuilder()
        buttons = InlineKeyboardBuilder()
        for i in range(len(data_per_page)):
            builder.button(
                text=f'{data_per_page[i]}', callback_data=ListView(
                    id=f'{self.id}',
                    current_page=self.current_page,
                    index=i+(self.page_number-1)*self.rows*self.columns,
                )
            )

    def get_max_page(self):
        return math.ceil(float(len(self.data)) / self.page_size)

    def has_more_than_one_page(self):
        return self.get_max_page() > 1

    def slice_data(self):
        start_index = (self.current_page-1) * self.page_size
        end_index = min(start_index + self.page_size, len(self.data))

        return self.data[start_index:end_index]

    def next(self):
        max_page = self.get_max_page()
        if max_page > 1:
            self.current_page = (self.current_page + 1) % max_page

        return self.slice_data()

    def previous(self):
        max_page = self.get_max_page()
        if max_page > 1:
            self.current_page = (self.current_page - 1) % max_page

        return self.slice_data()


def make_hash(lst: list, current_page: int) -> dict:
    hash_dict = dict()
    for i, element in enumerate(lst):
        hash_dict[i + 1 + current_page * 10] = element
    return hash_dict


async def print_list(message: Message, data: list, lv: ListView, lt: ListType, replacement: bool, bot: Bot):
    global active_listview_messages
    if not data:
        text = lv.empty_data_text
        if replacement:
            message_id = ... #get_listview_message(message.chat.id)
            chat_id = message.chat.id
            if lt == ListType.AUTO_ANALYZE_PAIRS:
                response = await bot.edit_message_text(text, chat_id=chat_id, message_id=message_id,
                                                       reply_markup=...)
            else:
                response = await bot.edit_message_text(text, chat_id=chat_id, message_id=message_id)
        else:
            if lt == ListType.AUTO_ANALYZE_PAIRS:
                response = await message.answer(text, reply_markup=...)
            else:
                response = await message.answer(text)

        # save_listview(message.chat.id, lv)
        # save_listview_message(message.chat.id, response.message_id)
        return

    text = '\n'
    text_hash = make_hash(data, lv.current_page)
    for key, value in text_hash.items():
        if lt == ListType.VERIFIED_USERS:
            value = value[1]
        elif lt == ListType.ACTIVE_REQUESTS:
            value = value[1]
        text += f'{key}. {value}\n\n'
    # save_listview(message.chat.id, lv)

    markup = ...
    text = text.replace("<", "")
    text = text.replace(">", "")

    if replacement:
        message_id = ... #get_listview_message(message.chat.id)
        chat_id = message.chat.id
        response = await bot.edit_message_text(lv.start_text + text + lv.end_text,
                                               chat_id=chat_id, message_id=message_id, reply_markup=markup)
    else:
        response = await message.answer(lv.start_text + text + lv.end_text,
                                        reply_markup=markup)
    # save_listview_message(message.chat.id, response.message_id)