from collections import UserList
from typing import Callable, Optional, List, TypeVar

T = TypeVar('T')


class ClusterList(UserList):
    def __init__(self, criterion: Callable[..., bool], merger: Callable[[T, T], T]) -> None:
        super().__init__()
        self.criterion = criterion
        self.merger = merger

    def append(self, item) -> None:
        for i, el in enumerate(self.data):
            if self.criterion(el, item):
                self.data[i] = self.merger(el, item)
                return
        super().append(item)

