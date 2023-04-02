import subprocess
from colorama import Fore
from ..base import VirtualEnv_Delete
from .goenv_checks import GoenvChecks
from nightcapcore import Printer
from nightcapcore.command.command import Command
# from nightcapcore.package.language.language import Language
from nightcapcore.package.information.package_information import PackageInformation
from nightcapcore.exceptions.virtenv.delete import VirtenvDeleteException
from nightcapcore.exceptions.virtenv.setup import *

class GoenvDeleteCommand(VirtualEnv_Delete, Command):
    def __init__(self, pkg_info: PackageInformation) -> None:
        super().__init__()
        self.pkg_info = pkg_info
        self.printer = Printer()

    def delete(self, env_name: str):
        try:
            _installed_at = subprocess.run(
                [
                    "goenv",
                    "which",
                    env_name
                ],
                capture_output=True                
            )
            # print("Remove shim from :: %s" % (str(_installed_at.stdout.decode())))
        
            _removed = subprocess.run(
                [
                    "rm",
                    str(_installed_at.stdout.decode()).strip()
                ],
                capture_output=True                
            )
            _rehashed = subprocess.run(
                [
                    "goenv",
                    "rehash"
                ],
                capture_output=True
            )
            # print("Removed from shims :: %s" % (str(_removed)))
            return True
        except VirtenvDeleteException as e:
            raise e

    def execute(self) -> dict:
        try:
            # _pyenvchecks = GoenvChecks()
            # try:
            #     _env_check = _pyenvchecks.check_env(self.pkg_info.entry_file)
            # except Exception as e:
            #     raise VirtenvCheckException("UNABLE TO CHECK GOENV ENVIRONMENTS")
                
            # if _env_check:
            self.printer.print_underlined_header("Removing Goenv")
            self.printer.item_1(f"{self.pkg_info.entry_file}")

            _deleted:bool = self.delete(self.pkg_info.entry_file)
            
            if _deleted:
                self.printer.print_formatted_check("Deleted Successfully")
            else:
                self.printer.print_formatted_check("Unable to find", optionaltext=f"{self.pkg_info.entry_file}", leadingText="[X]", leadingColor=Fore.RED)
        except Exception as e:
            raise e