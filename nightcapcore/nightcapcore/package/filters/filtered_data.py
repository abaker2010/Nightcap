from __future__ import annotations
from typing import Dict

class FilterData(object):
    def __init__(self, id: str, component_id: str, name: str, 
                        section_id: str, value: object) -> None:
        self.id = id
        self.component_id = component_id
        self.name = name
        self.section_id = section_id
        self.value = value

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(data: dict) -> FilterData:
        return FilterData(**data)