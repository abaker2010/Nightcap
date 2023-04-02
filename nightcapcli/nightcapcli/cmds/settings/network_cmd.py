# region Imports
from typing import List
from nightcapcli.base.base_cmd import NightcapBaseCMD
# endregion

class NightcapNetworkCMD(NightcapBaseCMD):
    # region Init
    def __init__(self, channelID: str = None) -> None:
        NightcapBaseCMD.__init__(self, ["settings", "system", "network"], channelid=channelID)

    # endregion
    def complete_select(self, text, line, begidx, endidx) -> List[str]:
        return [i for i in ("tor", "standard") if i.startswith(text)]

    def help_select(self) -> None:
        self.printer.help("Select the protocol to use for requests")
        self.printer.help("Useage: select <tor | standard>")

    def do_select(self, line) -> None:
        if str(line).lower() == "tor":
            print("Selecting tor")
        elif str(line).lower() == "standard":
            print("Selecting Standard")
        else:
            self.printer.print_error(
                Exception(
                    "Error selecting network. Please view the help to see options allowed."
                )
            )
