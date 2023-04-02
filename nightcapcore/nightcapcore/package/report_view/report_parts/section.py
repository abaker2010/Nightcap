from __future__ import annotations
from typing import Dict

class Section(object):
    def __init__(self, title: str, sid: int,
                         order: str, addproperties: Dict[str, object]) -> None:
        
        self.title = title
        self.sid = sid
        self.order = order
        self.addproperties = addproperties

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(data: dict) -> Section:
        return Section(**data)