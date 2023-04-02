from __future__ import annotations
from typing import Dict, List
from nightcapcore.package.report_view.report_parts.component import Component
from nightcapcore.package.report_view.report_parts.layout import Layout
from nightcapcore.package.report_view.report_parts.section import Section

class ReportView(object):
    def __init__(self, title:str, 
                    components:List[Component], 
                    slayouts:List[Section],
                    layout:Layout,
                ) -> None:
        self.title = title
        self.components = components
        self.slayouts = slayouts
        self.layout = layout

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(data: dict) -> ReportView:
        return ReportView(**data)