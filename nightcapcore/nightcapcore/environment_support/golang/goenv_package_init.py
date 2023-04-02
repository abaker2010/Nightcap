import os
import subprocess

from ..base import VirtualEnv_Init
from nightcapcore import Printer
from nightcapcore.command.command import Command
from nightcapcore.package.language.language import Language
from nightcapcore.package.information.package_information import PackageInformation

class GoenvPackageInitCommand(VirtualEnv_Init, Command):
    def __init__(self, lang: Language, package_location: str, package_info: PackageInformation) -> None:
        super().__init__()
        self.lang = lang
        self.package_location = package_location
        self.printer = Printer()
        self.package_info = package_info

        

    def install_requirements(self):
        try:    
            print(self.package_location)
            _currentdir = os.getcwd()
            print(_currentdir)
            os.chdir(self.package_location)

            subprocess.check_call(
                [
                    "goenv",
                    "exec",
                    "go",
                    "install",
                    "github.com/tomnomnom/assetfinder@latest"
                ]
            )
            _installed = subprocess.run(
                [
                    "goenv",
                    "rehash"
                ],
                capture_output=True
            )
            print(_installed)
            _installed = subprocess.run(
                [
                    "goenv",
                    "exec",
                    "assetfinder",
                    "--help"
                ],
                capture_output=True
            )
            print(_installed)
            print('Installed package')
            os.chdir(_currentdir)
            
            return True
        except Exception as e:
            raise e
        

    def execute(self) -> bool:
        try:
            return self.install_requirements()
        except Exception as e:
            raise e
