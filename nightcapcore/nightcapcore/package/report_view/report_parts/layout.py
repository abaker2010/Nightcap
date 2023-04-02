from __future__ import annotations
from typing import List

class Layout(object):
    def __init__(self, sorder: List[int]) -> None:
        self.sorder = sorder

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(data: dict) -> Layout:
        return Layout(**data)
