# region Imports
from nightcapcore import Printer
from nightcapcore.package import Package
from nightcapcore.command.command import Command
from nightcapcore.invoker.invoker import Invoker
from nightcappackages.classes.paths.paths import NightcapPackagesPaths
from nightcappackages.classes.paths.pathsenum import NightcapPackagesPathsEnum
from nightcapcore.exceptions.virtenv.setup import EnvSetupException
from nightcapcore.environment_support import PyenvSetUpCommand
from nightcapcore.environment_support import PyenvPackageInitCommand
# endregion

class NightcapPackageInstallPyenvPythonCommand(Command):
    # region Init
    def __init__(self, package: Package) -> None:
        super().__init__()
        self.printer = Printer()
        self.package = package
        self.package_install_location = NightcapPackagesPaths().generate_path(
            NightcapPackagesPathsEnum.PackagesBase,
            [
                self.package.package_for.module,
                self.package.package_for.submodule, 
                self.package.package_information.package_name
            ],
        )
    # endregion

    def execute(self) -> bool:
        try:
            self.printer.print_underlined_header("Checking Pyenv Support")
            _pyenv_invoker = Invoker()
            _pyenv = PyenvSetUpCommand(self.package.package_information.language)
            _pyenv_invoker.set_on_start(_pyenv)
            if _pyenv_invoker.execute():
                self.printer.print_underlined_header("Installing Pip Requirements")

                _requirenments_invoker = Invoker()
                _requirenments_invoker.set_on_start(PyenvPackageInitCommand(self.package.package_information.language, self.package_install_location))
                _installed = _requirenments_invoker.execute()

                if _installed: 
                    self.printer.print_formatted_check("Requirements Installed")
                    return True
                else:
                    raise EnvSetupException("ERROR INSTALLING PIP REQUIREMENTS :: FAILED TO INSTALL")
        except Exception as e:
            raise e