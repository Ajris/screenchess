from collections import UserList
from typing import Callable, Optional, List


class ClusterList(UserList):
    def __init__(self, criterion: Callable[..., bool], initlist: Optional[List] = None) -> None:
        super().__init__(initlist)
        self.criterion = criterion

    def append(self, item) -> None:
        for i in self.data:
            if self.criterion(i, item):
                return
        super().append(item)

