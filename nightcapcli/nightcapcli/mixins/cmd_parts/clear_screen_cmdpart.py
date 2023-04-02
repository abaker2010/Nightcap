from nightcapcli.mixins.cmd_parts.base import CMDPartBase
from nightcapcore import ScreenHelper

class ClearScreenCMDPart(CMDPartBase):
    def __init__(self) -> None:
        super().__init__()

    def help_clear(self) -> None:
        self.printer.help("Clear the screen")

    def do_clear(self, line) -> None:
        ScreenHelper().clearScr()