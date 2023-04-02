import subprocess
from colorama import Fore
from ..base import VirtualEnv_Delete
from .pyenv_checks import PyenvChecks
from nightcapcore import Printer
from nightcapcore.command.command import Command
from nightcapcore.package.language.language import Language
from nightcapcore.exceptions.virtenv.delete import VirtenvDeleteException
from nightcapcore.exceptions.virtenv.setup import *

class PyenvDeleteCommand(VirtualEnv_Delete, Command):
    def __init__(self, lang: Language) -> None:
        super().__init__()
        self.lang = lang
        self.printer = Printer()

    def delete(self, env_name: str):
        try:
            subprocess.check_call(
                [
                    "pyenv",
                    "virtualenv-delete",
                    "-f",
                    env_name
                ]
            )
        
            return True
        except VirtenvDeleteException as e:
            raise e

    def execute(self) -> dict:
        try:
            _pyenvchecks = PyenvChecks()
            try:
                _env_check = _pyenvchecks.check_env(self.lang.env_name)
            except Exception as e:
                raise VirtenvCheckException("UNABLE TO CHECK PYENV ENVIRONMENTS")
                
            if _env_check:
                self.printer.print_underlined_header("Removing Pyenv")
                self.printer.item_1(f"{self.lang.env_name}")

                _deleted:bool = self.delete(self.lang.env_name)
                
                if _deleted:
                    self.printer.print_formatted_check("Deleted Successfully")
            else:
                self.printer.print_formatted_check("Unable to find", optionaltext=f"{self.lang.env_name}", leadingText="[X]", leadingColor=Fore.RED)
        except Exception as e:
            raise e
        