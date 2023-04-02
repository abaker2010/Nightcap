import os
import subprocess
from ..base import VirtualEnv_Init
from nightcapcore import Printer
from nightcapcore.command.command import Command
from nightcapcore.package.language.language import Language

class PyenvPackageInitCommand(VirtualEnv_Init, Command):
    def __init__(self, lang: Language, package_location: str) -> None:
        super().__init__()
        self.lang = lang
        self.package_location = package_location
        self.printer = Printer()

    def _requirements(self) -> str:
        if self.lang.requirements_file != None:
            self.printer.item_1("Installing Requirements", endingBreaks=1)
            _requirement_file = os.path.join(self.package_location, self.lang.requirements_file)
        else:
            if self.lang.requirements != {}:
                _requires = []
                for pkg, ver in self.lang.requirements.items():
                    _requires.append("%s==%s" % (pkg, ver))
                _requirement_file = ' '.join(_requires)
        return _requirement_file

    def install_requirements(self, env_name: str, requirements: str, isFile: bool = False):
        try:
            if isFile:
                subprocess.check_call(
                        [
                            "pyenv",
                            "do",
                            "-e",
                            env_name,
                            "pip",
                            "install",
                            "-r",
                            requirements
                        ]
                    )
            else:
                subprocess.check_call(
                        [
                            "pyenv",
                            "do",
                            "-e",
                            env_name,
                            "pip",
                            "install",
                            requirements
                        ]
                    )
            return True
        except Exception as e:
            raise e

    def execute(self) -> dict:
        try:
            return self.install_requirements(self.lang.env_name, self._requirements(), (True if self.lang.requirements_file != None else False))
        except Exception as e:
            raise e
