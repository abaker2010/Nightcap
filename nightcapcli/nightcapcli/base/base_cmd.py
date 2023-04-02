# region Imports
from cmd import Cmd
from colorama import Fore, Style
from nightcapcore import NightcapCLIConfiguration, KeyboardInterruptHandler
from nightcapcli.mixins.cmd_parts.banner_cmdpart import BannerCMDPart
from nightcapcli.mixins.cmd_parts.clear_screen_cmdpart import ClearScreenCMDPart
from nightcapcli.mixins.cmd_parts.config_cmdpart import ConfigCMDPart
from nightcapcli.mixins.cmd_parts.exit_cmdpart import ExitCMDPart
# endregion



class NightcapBaseCMD(Cmd, BannerCMDPart, ClearScreenCMDPart, ConfigCMDPart, \
                        ExitCMDPart):
    """
    This class is used as the base cmd for the program

    ...

    Attributes
    ----------
        selectedList:
            List for the consolses [<T>][<T>]

        channleID:
            The channel for the object

        config:
            NightcapCLIConfiguration, this is the main one for the program

        verbosity:
            Verbosity for the console printing

    Methods
    -------
        emptyline(self):
            Override to keep the enter key cleaned up

        preloop(self):
            Override for the preloop before entering into the cmd

        postcmd(self, stop: bool, line: str) -> bool:
            Override for after the command is done but the user does not have control yet

        postloop(self) -> None:
            Override for after the cmd loop is exiting
    """

    # region Init
    def __init__(self, selectedList: list, channelid=None) -> None:
        Cmd.__init__(self, completekey="tab", stdin=None, stdout=None)
        BannerCMDPart.__init__(self)
        ClearScreenCMDPart.__init__(self)
        ConfigCMDPart.__init__(self)
        ExitCMDPart.__init__(self)
        
        self.config = NightcapCLIConfiguration()

        self.selectedList = selectedList

        self.doc_header = Fore.GREEN + "Commands" + Style.RESET_ALL
        self.misc_header = Fore.GREEN + "Other" + Style.RESET_ALL
        self.undoc_header = Fore.GREEN + "System" + Style.RESET_ALL
        self.ruler = Fore.YELLOW + "-" + Style.RESET_ALL

        self.channelID = channelid
        self.prompt = self._prompt()
        self.channels = {}
        KeyboardInterruptHandler().reset_count()
    # endregion

    # region
    def _prompt(self) -> str:
        _p = []
        for _ in self.selectedList:
            _p.append("[" + Fore.LIGHTYELLOW_EX + _ + Fore.LIGHTGREEN_EX + "]")
        _p = "".join(_p)
        return Fore.GREEN + "nightcap" + _p + " > " + Fore.CYAN
    # endregion

    #region CMD Loop
    def cmdloop(self, intro=None) -> None:
        try:
            return super().cmdloop(intro)
        except KeyboardInterrupt as ke:
            if KeyboardInterruptHandler().interrupt():
                raise ke           
            else:
                print("")
                self.cmdloop(intro)
    #endregion

    # region CMD Overrides
    def emptyline(self) -> None:
        pass

    # putting into place to be used later
    def preloop(self) -> None:
        return super().preloop()

    def postcmd(self, stop: bool, line: str) -> bool:
        return super().postcmd(stop, line)

    def postloop(self) -> None:
        return super().postloop()

    # endregion
    #####

    # region Help
    def do_help(self, line) -> None:
        super(NightcapBaseCMD, self).do_help(line)
    # endregion
