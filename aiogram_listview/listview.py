import math
from enum import Enum
from typing import List, Any, Optional, Callable


class ListType(Enum):
    TYPE1 = "TYPE1"
    TYPE2 = "TYPE2"
    TYPE3 = "TYPE3"


class ListView:
    def __init__(
        self,
        data_list: List[Any],
        id: str,
        page_size: int = 10,
        current_page: int = 1,
        start_text: str = "Data list:\n\n",
        end_text: str = "\nSelect one of the options below👇",
        empty_data_text: str = "No data found!",
        is_show_page: bool = True,
        is_show_content_instead_of_indexes: bool = False,
        formatter: Optional[Callable[[int, Any], str]] = None
    ):
        self._id = id
        self._data = data_list
        self._page_size = page_size
        self._current_page = current_page
        self._start_text = start_text
        self._end_text = end_text
        self._empty_data_text = empty_data_text
        self._is_show_page = is_show_page
        self._is_show_content_instead_of_indexes = is_show_content_instead_of_indexes
        self._formatter = formatter

    def get_max_page(self) -> int:
        if not self._data:
            return 1
        return math.ceil(len(self._data) / self._page_size)

    def has_more_than_one_page(self) -> bool:
        return self.get_max_page() > 1

    def slice_data(self):
        max_page = self.get_max_page()
        if self._current_page > max_page:
            self._current_page = max_page
        if self._current_page < 1:
            self._current_page = 1

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

    def get_display_text(self) -> str:
        data_per_page, start_index, end_index = self.slice_data()
        if not data_per_page:
            return self._empty_data_text

        text = self._start_text
        for i, value in enumerate(data_per_page):
            idx = start_index + i + 1
            if self._formatter:
                line = self._formatter(idx, value)
            else:
                line = f'{idx}. {value}'
            text += f'{line}\n'
        
        text += self._end_text
        
        if self._is_show_page and self.has_more_than_one_page():
            text += f"\n\nPage {self._current_page}/{self.get_max_page()}"

        return text
