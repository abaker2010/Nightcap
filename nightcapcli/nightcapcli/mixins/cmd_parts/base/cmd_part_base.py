from abc import ABC
from nightcapcore import Printer

class CMDPartBase(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.printer = Printer()