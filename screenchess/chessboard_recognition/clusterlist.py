from collections import UserList, defaultdict
from typing import Callable, TypeVar
import numpy

T = TypeVar('T')


class ClusterList(UserList):
    def __init__(self, criterion: Callable[..., bool], merger: Callable[[T, T], T]) -> None:
        super().__init__()
        self.criterion = criterion
        self.merger = merger
        self.hits = defaultdict(int)

    def append(self, item) -> None:
        for i, el in enumerate(self.data):
            if self.criterion(el, item):
                self.data[i] = self.merger(el, item)
                self.hits[i] += 1
                return
        super().append(item)
        self.hits[len(self.data) - 1] += 1

    def trim(self, n: int) -> None:
        for k, v in self.hits.items():
            if v < n:
                self.data[k] = self.hits[k] = None
        self.data = list(filter(None, self.data))
