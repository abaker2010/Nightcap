from __future__ import annotations
from typing import Dict, List

class ReportViewComponent(object):
    def __init__(self, data: dict) -> None:
        self.id = data['id']
        self.design = data['design']
        self.flex = data['flex']
        self.children:List[ReportViewComponent] = None
        self.value = data['value']

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(data: dict) -> ReportViewComponent:
        return ReportViewComponent(data)