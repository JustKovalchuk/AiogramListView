from typing import Dict, Optional, Protocol
from aiogram_listview.listview import ListView

class BaseListViewStorage(Protocol):
    """Інтерфейс для сховища ListView. Будь-яке кастомне сховище має його наслідувати."""
    async def save_listview(self, user_id: int, lv: ListView) -> None: ...
    async def save_listview_message(self, user_id: int, list_id: str, message_id: int) -> None: ...
    async def get_listview(self, user_id: int, list_id: str) -> Optional[ListView]: ...
    async def get_listview_message(self, user_id: int, list_id: str) -> Optional[int]: ...
    async def clear_listview(self, user_id: int, list_id: str) -> None: ...

class MemoryListViewStorage:
    """Дефолтна реалізація в оперативній пам'яті."""
    def __init__(self):
        self.active_listviews: Dict[tuple, ListView] = {}
        self.active_listview_messages: Dict[tuple, int] = {}

    async def save_listview(self, user_id: int, lv: ListView) -> None:
        self.active_listviews[(user_id, lv.id)] = lv

    async def save_listview_message(self, user_id: int, list_id: str, message_id: int) -> None:
        self.active_listview_messages[(user_id, list_id)] = message_id

    async def get_listview(self, user_id: int, list_id: str) -> Optional[ListView]:
        return self.active_listviews.get((user_id, list_id))

    async def get_listview_message(self, user_id: int, list_id: str) -> Optional[int]:
        return self.active_listview_messages.get((user_id, list_id))

    async def clear_listview(self, user_id: int, list_id: str) -> None:
        self.active_listviews.pop((user_id, list_id), None)
        self.active_listview_messages.pop((user_id, list_id), None)
