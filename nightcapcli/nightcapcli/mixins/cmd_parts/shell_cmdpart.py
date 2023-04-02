import os
from colorama import Fore, Style
from nightcapcli.mixins.cmd_parts.base import CMDPartBase

class ShellCMDPart(CMDPartBase):
    def __init__(self) -> None:
        super().__init__()

    # region Shell
    def help_shell(self) -> None:
        self.printer.help("Execute commands on the host system or container")

    def do_shell(self, s) -> None:
        "\n\tRun a shell command, becareful with this. This feature is still in beta\n"
        print(Fore.LIGHTGREEN_EX)
        os.system(s)
        print(Style.RESET_ALL)
    # endregion