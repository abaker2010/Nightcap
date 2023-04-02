# region Imports
import os
from git import repo
from typing import List
from nightcapcore.command.command import Command
from nightcapcore.package import Package
from nightcapcore import Printer
from nightcapcore.database.mongo.mongo_packages import MongoPackagesDatabase
# endregion

class NightcapPackageGitUpdateCommand(Command):
    def __init__(self, packges: List[Package]) -> None:
        super().__init__()
        self.printer = Printer()
        self.packages = packges
        self.pkg_db = MongoPackagesDatabase()

    def execute(self) -> dict:
        self.printer.item_1("Packages to update", len(self.packages))

        for pkg in self.packages:
            try:
                self.printer.print_formatted_additional("Updating", pkg.package_information.package_name)
                _repo_path = os.sep.join(self.pkg_db.get_package_run_path(pkg).split(os.sep)[:-1])
                _pkg_repo = repo.Repo(_repo_path)
                # _pulled = _pkg_repo.remote().pull()
                _pkg_repo.head.reset()

                # # _pulled = _pkg_repo.remotes.pull()
                # print(type(_pulled))
                # print(_pulled)
                # for _pull in _pulled:
                #     print(_pull)                    
                    
                self.printer.print_formatted_check("Successful", leadingTab=3)
            except Exception as e:
                self.printer.print_error(Exception(f"Failed to update :: {pkg.package_information.package_name} :: {e}"))
            