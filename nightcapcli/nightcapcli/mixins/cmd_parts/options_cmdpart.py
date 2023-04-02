from typing import List
from nightcapcli.mixins.cmd_parts.base import CMDPartBase
from nightcapcli.generator import NightcapOptionGenerator
from nightcapcore.database.mongo.mongo_report import MongoReportDatabase

class OptionsCMDPart(CMDPartBase):
    def __init__(self, selectedList: List[str] = None) -> None:
        super().__init__()
        self.selectedList = selectedList

    # region Help Options
    def help_options(self) -> None:
        self.printer.help("See what options are available to use. Use -d on packages to see detailed information")
    # endregion

    # region Do Options
    def do_options(self, line) -> None:
        # """\nSee what options are available to use. Use -d on packages to see detailed information\n"""
        if line == '':
            NightcapOptionGenerator(self.selectedList).options()
        elif line == "-d":
            NightcapOptionGenerator(self.selectedList).options(isDetailed=True)
        else:
            self.printer.print_error(Exception("ERROR GETTING OPTIONS"))
    # endregion
