# region Imports
from typing import List
from nightcapcore.helpers import ScreenHelper
from nightcapcore.package import Package
from nightcapcore.invoker import Invoker
from nightcapcore.database.mongo.mongo_packages import MongoPackagesDatabase

from nightcapcli.base.base_cmd import NightcapBaseCMD
from nightcapcli.completer.tab_completer import NightcapTabCompleter
from nightcapcli.generator.listpackages import NightcapListPackages
from nightcappackages.classes.commands import NightcapPackageInstallerCommand,\
                                                NightcapPackageUninstallerCommand, \
                                                NightcapUpdaterRebootCommand, \
                                                NightcapPackageGitUpdateCommand
# endregion


class NightcapPackagesCMD(NightcapBaseCMD):
    # region Init
    def __init__(self, channelID: str = None) -> None:
        NightcapBaseCMD.__init__(self, ["settings", "packages"], channelid=channelID)
        # self.task_manager = TaskManager()
        self.uninstallList = []
    
    # endregion

    # region Install
    def do_install(self, line) -> None:
        try:
            if len(line.strip()) == 0:
                raise Exception("Please provide a NCP to install")
            else:
                invoker = Invoker()
                invoker.set_on_start(NightcapPackageInstallerCommand(line))
                invoker.execute()
        except Exception as e:
            self.printer.print_error(e)

    def help_install(self) -> None:
        self.printer.help(
            "Install a new module. Formatting for module creation can be found at",
            "https://some_url.com",
        )

    # endregion

    # region Uninstall
    def do_uninstall(self, line) -> None:
        try:
            invoker = Invoker()
            invoker.set_on_start(NightcapPackageUninstallerCommand(line))
            invoker.execute()
        except Exception as e:
            self.printer.print_error(e)

    def help_uninstall(self) -> None:
        self.printer.help("Uninstall a module example", "uninstall [package_path]")

    def complete_uninstall(self, text, line, begidx, endidx) -> list:
        try:
            return NightcapTabCompleter().complete(
                self.uninstallList, text, line.replace("uninstall ", "")
            )
        except Exception as e:
            print(e)
    # endregion

    # region List Packages
    def help_list(self) -> None:
        self.printer.help("List installed packages")

    def do_list(self, line) -> None:
        ScreenHelper().clearScr()
        NightcapListPackages().list_packages()
    # endregion

    # region Update
    def help_update(self) -> None:
        self.printer.help(
            "Update the program, if there is no option specified the default will be used.",
            "update [main|dev] [-v]",
        )

    def do_update(self, line) -> None:
        invoker = Invoker()
        invoker.set_on_finish(NightcapUpdaterRebootCommand())

        try:
            self.printer.print_underlined_header("Updating Github Repo(s)")
            package_db = MongoPackagesDatabase()
            _github_packages:List[Package] = []
            _db_packages = package_db.get_all_github()

            if _db_packages.count() != 0:
                for p in _db_packages:
                    _github_packages.append(Package(p))
            else:
                self.printer.print_formatted_check("No packages to update")

            invoker.set_on_start(NightcapPackageGitUpdateCommand(_github_packages))
            invoker.execute()
        except Exception as e:
            if e.args[0] == "Restarting":
                raise KeyboardInterrupt("Restarting")
            else:
                self.printer.print_error(e)
    # endregion