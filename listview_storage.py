from listview import ListView

class ListViewStorage:
    active_listviews = dict()
    active_listview_messages = dict()

    def save_listview(self, tg_id, lv: ListView):
        self.active_listviews.update({tg_id: lv})

    def save_listview_message(self, tg_id, message_id: int):
        self.active_listview_messages.update({tg_id: message_id})

    def get_listview(self, tg_id):
        return self.active_listviews.get(tg_id)

    def get_listview_message(self, tg_id):
        return self.active_listview_messages.get(tg_id)

    def clear_listview(self, tg_id):
        self.active_listviews.pop(tg_id)
        self.active_listview_messages.pop(tg_id)
