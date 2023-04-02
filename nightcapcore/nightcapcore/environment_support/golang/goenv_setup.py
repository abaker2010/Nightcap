import subprocess
from colorama import Fore
from nightcapcore import Printer
from ..base import VirtualEnv_Setup
from .goenv_checks import GoenvChecks
# from .pyenv_checks import PyenvChecks
from nightcapcore.command.command import Command
from nightcapcore.package.language.language import Language
from nightcapcore.exceptions.virtenv.setup import *

class GoenvSetupCommand(VirtualEnv_Setup, Command):  
    def __init__(self, lang: Language) -> None:
        super().__init__()
        self.lang = lang
        self.printer = Printer()

    def create_env(self):
        return super().create_env()
    
    def update_new_env(self):
        return super().update_new_env()
    
    def install_version(self, env_version: str) -> bool:
        self.printer.item_1("NOTE", "Please be patient this may take awhile..")
        subprocess.check_call(
                [
                    "goenv",
                    "install",
                    env_version
                ]
            )
        return True
    
    def execute(self) -> bool:
        try:
            _goenvchecks = GoenvChecks()
            try:
                _clean_version = _goenvchecks.clean_version(self.lang.version)
                self.printer.print_formatted_additional("GO Version :: %s" % (_clean_version))
            except Exception as e:
                raise VirtenvVersionCheckException(e)
            
            try:
                _ver_check = _goenvchecks.check_version_installed(_clean_version)
                self.printer.print_formatted_additional("Version Exists :: %s" % (_ver_check))
            except Exception as e:
                raise VirtenvVersionCheckException("UNABLE TO CHECK GOENV VERSIONS INSTALLED")
            
            if _ver_check:
                self.printer.print_formatted_check("Version", optionaltext=f"{_clean_version} Exists")
                return True
            else:
                self.printer.print_formatted_check("Version", optionaltext=f"{_clean_version} Needs Installed", leadingText="[X]", leadingColor=Fore.RED)
                try:
                    _go_version_available = _goenvchecks.check_version_downloadable(_clean_version)
                    if _go_version_available:
                        self.printer.print_formatted_additional("Go Version Can Be Downloaded")
                    else:
                        self.printer.print_formatted_additional("Go Version Can Not Be Downloaded")
                except Exception as e:
                    raise e
                
                try:
                    if _go_version_available:
                        _installed = self.install_version(_clean_version)
                        if _installed:
                            self.printer.print_formatted_additional("Go Version Installed :: %s" % (_installed))
                            return True
                        else:
                            raise VirtenvVersionInstallException(f"ERROR INSTALLING GOENV VERSION ({_clean_version})")
                except Exception as e:
                    raise e
            
            
            
        except Exception as e:
            raise Exception("ERROR WITH GOENV SETUP :: %s" % (str(e)))