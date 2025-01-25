import math
from enum import Enum


class ListType(Enum):
    TYPE1 = "TYPE1"
    TYPE2 = "TYPE2"
    TYPE3 = "TYPE3"


class ListView:
    def __init__(self, data_list: list, id: str, page_size: int = 10, current_page: int = 1,
                 start_text="Data list:\n\n", end_text="\nSelect one of the options below👇", empty_data_text="No data found!",
                 is_show_page=True, is_show_content_instead_of_indexes=False):
        self._id = id
        self._data = data_list
        self._page_size = page_size

        self._current_page = current_page

        self._start_text = start_text
        self._end_text = end_text
        self._empty_data_text = empty_data_text
        self._is_show_page = is_show_page
        self._is_show_content_instead_of_indexes = is_show_content_instead_of_indexes

    def __str__(self):
        return f"""Data: {self._data}\n
                   Current page: {self._current_page}\n
                   """

    def my_init(self):
        data_per_page, start_index, end_index = self.slice_data()
        return data_per_page

    def get_max_page(self):
        tmp = math.ceil(float(len(self._data)) / self._page_size)
        return tmp

    def has_more_than_one_page(self):
        return self.get_max_page() > 1

    def slice_data(self):
        start_index = (self._current_page - 1) * self._page_size
        end_index = min(start_index + self._page_size, len(self._data))

        return self._data[start_index:end_index], start_index, end_index

    def next(self):
        max_page = self.get_max_page()
        if max_page > 1:
            self._current_page = self._current_page % max_page + 1

        return self.slice_data()

    def previous(self):
        max_page = self.get_max_page()
        if max_page > 1:
            self._current_page = self._current_page - 1
            if self._current_page <= 0:
                self._current_page = max_page

        return self.slice_data()

    def get_display_text(self):
        data_per_page, start_index, end_index = self.slice_data()
        text = self._empty_data_text
        if len(data_per_page) > 0:
            text = self._start_text
            for i, value in enumerate(data_per_page):
                text += f'{start_index + i + 1}. {value}\n'
            text += self._end_text

        # if self._is_show_page:
        #     text += f"page {self._current_page}/{self.get_max_page()}"

        return text
