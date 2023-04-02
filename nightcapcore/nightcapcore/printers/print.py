
from nightcapcore.printers import (
    InputPrinter,
    ItemPrinter,
    HeaderPrinter,
    ErrorPrinter,
    CheckMarkPrinter,
    DebugPrinter,
    TablePrinter,
    WaitingPrinter
)

class Printer(
    CheckMarkPrinter,
    ErrorPrinter,
    HeaderPrinter,
    ItemPrinter,
    InputPrinter,
    WaitingPrinter,
    DebugPrinter,
    TablePrinter
):
    def __init__(self) -> None:
        super().__init__()
