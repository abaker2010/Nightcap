from nightcapcli.mixins.cmd_parts.base import CMDPartBase
from colorama import Fore, Style
from nightcapcore import ScreenHelper
from nightcapcore.configuration.configuration import NightcapCLIConfiguration

class ConfigCMDPart(CMDPartBase):
    def __init__(self) -> None:
        super().__init__()
        self.config = NightcapCLIConfiguration()

    # region Config
    def help_config(self) -> None:
        self.printer.help("Get the current system configuration(s)")

    def do_config(self, line) -> None:
        ScreenHelper().clearScr()
        self.printer.print_underlined_header_undecorated("Configuration")

        self.printer.print_underlined_header("Verbosity", leadingTab=2)
        self.printer.print_formatted_other(
            "Verbosity",
            "Normal" if self.config.verbosity == False else "Debug",
            leadingTab=3,
            optionalTextColor=Fore.LIGHTBLACK_EX
            if self.config.verbosity == False
            else Fore.LIGHTYELLOW_EX,
        )

        self.printer.print_underlined_header("Database (Mongo)", leadingTab=2)
        self.printer.print_formatted_other(
            "URL",
            self.config.config["MONGOSERVER"]["ip"],
            leadingTab=3,
            optionalTextColor=Fore.YELLOW,
        )
        self.printer.print_formatted_other(
            "Status",
            self.config.config["MONGOSERVER"]["port"],
            leadingTab=3,
            optionalTextColor=Fore.YELLOW,
            endingBreaks=1,
        )

        self.printer.print_underlined_header("Project Selected", leadingTab=2)
        if self.config.project != None:
            self.printer.print_formatted_additional("Name", self.config.project.name, leadingTab=3, endingBreaks=1)
        else:
            self.printer.print_formatted_additional("No Project Selected", leadingTab=3, endingBreaks=1)

    # endregion