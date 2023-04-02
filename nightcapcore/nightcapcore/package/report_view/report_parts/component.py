from __future__ import annotations
from typing import Dict

class Component(object):
    def __init__(self, id: str, type: str, properties: Dict[str, object]) -> None:
        self.id = id
        self.type = type
        self.properties = properties

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(data: dict) -> Component:
        return Component(**data)