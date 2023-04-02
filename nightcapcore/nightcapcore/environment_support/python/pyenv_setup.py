import subprocess
from colorama import Fore
from nightcapcore import Printer
from ..base import VirtualEnv_Setup
from .pyenv_checks import PyenvChecks
from nightcapcore.command.command import Command
from nightcapcore.package.language.language import Language
from nightcapcore.exceptions.virtenv.setup import *

class PyenvSetUpCommand(VirtualEnv_Setup, Command):
    def __init__(self, lang: Language) -> None:
        super().__init__()
        self.lang = lang
        self.printer = Printer()

    def create_env(self, env_version: str, env_name: str) -> bool:
        subprocess.check_call(
                [
                    "pyenv",
                    "virtualenv",
                    env_version, 
                    env_name
                ]
            )
        return True

    def update_new_env(self, env_name: str) -> bool:
        subprocess.check_call(
                [
                    "pyenv",
                    "do",
                    "-e", 
                    env_name,
                    "pip",
                    "install",
                    "--upgrade",
                    "pip"
                ]
            )
        return True

    def install_version(self, env_version: str) -> bool:
        self.printer.item_1("NOTE", "Please be patient this may take awhile..")
        subprocess.check_call(
                [
                    "pyenv",
                    "install",
                    env_version
                ]
            )
        return True

    def execute(self) -> bool:
        try: 
            _pyenvchecks = PyenvChecks()
            try:
                _clean_version = _pyenvchecks.clean_version(self.lang.version)
            except Exception as e:
                raise VirtenvVersionCheckException(e)

            try:
                _ver_check = _pyenvchecks.check_version_installed(_clean_version)
            except Exception as e:
                raise VirtenvVersionCheckException("UNABLE TO CHECK PYENV VERSIONS INSTALLED")

            try:
                _env_check = _pyenvchecks.check_env(self.lang.env_name)
            except Exception as e:
                raise VirtenvCheckException("UNABLE TO CHECK PYENV ENVIRONMENTS")

            if _ver_check:
                self.printer.print_formatted_check("Version", optionaltext=f"{_clean_version} Exists")
            else:
                self.printer.print_formatted_check("Version", optionaltext=f"{_clean_version} Needs Installed", leadingText="[X]", leadingColor=Fore.RED)
                try:
                    _py_version_available = _pyenvchecks.check_version_downloadable(_clean_version)
                    if _py_version_available == False:
                        raise VirtenvVersionInstallException(f"PYENV DOES NOT SUPPORT VERSION ({_clean_version}) :: CHECK ALLOWED PYENV VERSIONS (pyenv install -l)")
                except Exception as e:
                    raise e
                try:
                    if _py_version_available:
                        self.install_version(_clean_version)
                except Exception as e:
                    raise VirtenvVersionInstallException(f"ERROR INSTALLING PYENV VERSION ({_clean_version})")
            
            if _env_check:
                self.printer.print_formatted_check("Env", optionaltext=f"{self.lang.env_name} Exists", leadingText="[X]", leadingColor=Fore.RED)
                raise VirtenvCreateException("PYENV ENV ALREADY EXISTS :: REMOVE CURRENT ENV BEFORE INSTALLING")
            else:
                self.printer.print_formatted_check("Env", optionaltext=f"{self.lang.env_name} Needs Created")
                try:
                    self.create_env(_clean_version, self.lang.env_name)
                    self.update_new_env(self.lang.env_name)
                except Exception as e:
                    raise VirtenvCreateException(f"ERROR CREATING ENV ({self.lang.env_name}) :: VER ({_clean_version})")

            return True
        except Exception as e:
            raise e