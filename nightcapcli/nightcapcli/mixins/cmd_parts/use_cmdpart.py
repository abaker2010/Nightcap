from typing import List
from nightcapcli.observer import CLIPublisher
from nightcapcli.mixins.cmd_parts.base import CMDPartBase
from nightcapcore.exceptions.publisher import PublisherException
from nightcapcli.completer.tab_completer import NightcapTabCompleter

class UseCMDPart(CMDPartBase):
    def __init__(self, selectedList: List[str] = None) -> None:
        super().__init__()
        self.selectedList = selectedList

    # region Help Use
    def help_use(self) -> None:
        self.printer.help(
            "Select/Use a module/submobule/package: use [module/submobule/package name]\n"
        )

    # endregion

    # region Complete Use
    def complete_use(self, text, line, begidx, endidx) -> list:
        try:
            return NightcapTabCompleter().complete(
                self.selectedList, text, line.replace("use ", "")
            )
        except Exception as e:
            self.printer.print_error(e)
    # endregion

    # region Do Use
    def do_use(self, line: str, override: object = None) -> None:
        try:
            if len(line.strip()) == 0:
                raise Exception("Please provide a path to use")
            else:
                _current_loc = True if line.startswith("/") else False

                if _current_loc:
                    line = line.replace('/', '', 1)

                _new_opts:List[str] = []
                if len(line) != 0:
                    _new_opts = line.split('/')
                else:
                    _new_opts = []
                CLIPublisher().pub({"page_add" : _new_opts})
        except PublisherException as pe:
            self.printer.print_error(f"VALIDATION FAILURE :: {pe}")
        except Exception as e:
            self.printer.print_error(f"{e}")
    # endregion
