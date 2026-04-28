from typing import Dict, Optional, Any
from aiogram_listview.listview import ListView

class ListViewStorage:
    def __init__(self):
        # Key: (user_id, list_id)
        self.active_listviews: Dict[tuple, ListView] = {}
        # Key: (user_id, list_id)
        self.active_listview_messages: Dict[tuple, int] = {}

    def save_listview(self, user_id: int, lv: ListView):
        self.active_listviews[(user_id, lv._id)] = lv

    def save_listview_message(self, user_id: int, list_id: str, message_id: int):
        self.active_listview_messages[(user_id, list_id)] = message_id

    def get_listview(self, user_id: int, list_id: str) -> Optional[ListView]:
        return self.active_listviews.get((user_id, list_id))

    def get_listview_message(self, user_id: int, list_id: str) -> Optional[int]:
        return self.active_listview_messages.get((user_id, list_id))

    def clear_listview(self, user_id: int, list_id: str):
        self.active_listviews.pop((user_id, list_id), None)
        self.active_listview_messages.pop((user_id, list_id), None)
