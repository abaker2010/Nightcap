from nightcapcore.printers import Printer
from bson.objectid import ObjectId
from typing import List

class Task(object):
    def __init__(self, _id: ObjectId, name: str, packages: List[dict]) -> None:
        self._id = _id
        self.name = name
        self.printer = Printer()

    def run(self): 
        self.printer.item_2("Running Task")

    def __str__(self) -> str:
        return "%s" % self.name