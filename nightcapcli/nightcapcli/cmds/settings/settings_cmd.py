# region Imports
from typing import List

from nightcapcore.configuration.configuration import NightcapCLIConfiguration

from nightcapcli.base.base_cmd import NightcapBaseCMD
from nightcapcli.cmds.settings.system_cmd import NightcapSystemCMD
from nightcapcli.cmds.settings.network_cmd import NightcapNetworkCMD
from nightcapcli.cmds.settings.backup_cmd import NightcapBackupsCMD
from nightcapcli.cmds.settings.packages_cmd import NightcapPackagesCMD
from nightcapcli.cmds.settings.cmd_dev_options import NightcapDevOptionsCMD
from nightcapcli.cmds.settings.network_config_cmd import NightcapMongoNetworkSettingsCMD
# endregion

class NightcapSettingsCMD(NightcapBaseCMD):
    """
    (User CLI Object)

    This class is used as the cli for the user settings

    ...

    Attributes
    ----------


    Methods
    -------
        Accessible
        -------

            help_devoptions(self): -> None
                Override for the devoptions help command

            do_dev(self, line): -> None
                Allows the user to enter into the devoptions cmd

            help_list(self): -> None
                Override for the list help command

            do_list(self, line): -> None
                Lists all of the packages installed

            help_database(self): -> None
                Override for the server help command

            do_database(self, line): -> None
                Allows the user to enter into the server cmd

            complete_verbosity(self, text, line, begidx, endidx): -> None
                Tab auto complete options for the verbosity command

            help_verbosity(self): -> None
                Override for the verbose help command

            do_verbosity(self, line): -> None
                Allows the user to change the verbostiy of the output shown in the console

    """

    # region Init
    def __init__(self, channelID: str = None) -> None:
        NightcapBaseCMD.__init__(self, ["settings"], channelid=channelID)
        self.uninstallList = []
    # endregion


    # region System Options
    def help_system(self) -> None:
        self.printer.help("System Settings")

    def do_system(self, line) -> None:
        NightcapSystemCMD("system_settings").cmdloop()
        # NightcapDevOptionsCMD(["settings", "dev"], "devoptions").cmdloop()
    # endregion


    # region Dev Options
    def help_dev(self) -> None:
        self.printer.help("Developer Options")

    def do_dev(self, line) -> None:
        NightcapDevOptionsCMD(["settings", "dev"], "devoptions").cmdloop()
    # endregion

    # region Packages Option
    def help_packages(self) -> None:
        self.printer.help("Un/Install/List Packages")

    def do_packages(self, line) -> None:
        try:
            NightcapPackagesCMD(line).cmdloop()
        except Exception as e:
            self.printer.print_error(e)
    # endregion

    # region Verbosity
    def complete_verbosity(self, text, line, begidx, endidx) -> List[str]:
        return [i for i in ("normal", "debug") if i.startswith(text)]

    def help_verbosity(self) -> None:
        self.printer.help("Configure verbosity level", endingBreaks=0)
        self.printer.help("Usage: verbosity <normal|debug>", leadingBreaks=0)

    def do_verbosity(self, line) -> None:
        try:
            if line != "":
                if "normal" == str(line).lower().strip():
                    
                    self.config.config.set("NIGHTCAPCORE", "verbose", "False")
                    self.config.verbosity = False
                elif "debug" == str(line).lower().strip():
                    self.config.config.set("NIGHTCAPCORE", "verbose", "True")
                    self.config.verbosity = True

                self.config.save()
                print(self.config.verbosity)
                print(NightcapCLIConfiguration().verbosity)
            else:
                raise Exception(
                    "Error with level, for more information use: help verbosity"
                )
        except Exception as e:
            self.printer.print_error(e)
    # endregion

    # region Database
    def help_database(self) -> None:
        self.printer.help("Configure a server")
        self.printer.help("Usage: server <web|database>")

    def do_database(self, line) -> None:
        try:
            NightcapMongoNetworkSettingsCMD().cmdloop()
        except Exception as e:
            self.printer.print_error(e)
    # endregion

    # region Exit
    def do_exit(self, line) -> bool:
        return True
    # endregion
