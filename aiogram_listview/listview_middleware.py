# listview_middleware.py
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram_listview.listview_storage import BaseListViewStorage

class ListViewMiddleware(BaseMiddleware):
    def __init__(self, storage: BaseListViewStorage):
        self.storage = storage

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Прокидаємо сховище у параметри хендлерів
        data['listview_storage'] = self.storage
        return await handler(event, data)