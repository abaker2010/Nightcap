
from nightcapcore import Printer
from nightcapcore.package import Package
from nightcapcore.command.command import Command
from nightcapcore.invoker.invoker import Invoker
from nightcapcore.environment_support import GoenvSetupCommand, GoenvPackageInitCommand
from nightcapcore.exceptions.virtenv.setup import EnvSetupException 
from nightcappackages.classes.paths.paths import NightcapPackagesPaths
from nightcappackages.classes.paths.pathsenum import NightcapPackagesPathsEnum


class NightcapPackageInstallerGoenvCommand(Command):
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

    def execute(self) -> bool:
        try:
            self.printer.print_underlined_header("Checking Goenv Support")

            # return True
            _goenv_invoker = Invoker()
            _goenv = GoenvSetupCommand(self.package.package_information.language)
            _goenv_invoker.set_on_start(_goenv)

            if _goenv.execute():
                self.printer.print_underlined_header("Installing Go Requirements")
                _goetup_invoker = Invoker()
                _goetup_invoker.set_on_start(GoenvPackageInitCommand(self.package.package_information.language, self.package_install_location, self.package.package_information))
                if _goetup_invoker.execute():
                    self.printer.print_formatted_additional("INSTALLED INTO GOENV")
                    return True
                else:
                    raise EnvSetupException("ERROR INSTALLING INTO GOENV :: FAILED TO INSTALL")
            else:
                raise EnvSetupException("ERROR INSTALLING GO :: FAILED TO INSTALL")
            # _pyenv_invoker = Invoker()
            # _pyenv = PyenvSetUpCommand(self.package.package_information.language)
            # _pyenv_invoker.set_on_start(_pyenv)
            # if _pyenv_invoker.execute():
            #     self.printer.print_underlined_header("Installing Pip Requirements")

            #     _requirenments_invoker = Invoker()
            #     _requirenments_invoker.set_on_start(PyenvPackageInitCommand(self.package.package_information.language, self.package_install_location))
            #     _installed = _requirenments_invoker.execute()

            #     if _installed: 
            #         self.printer.print_formatted_check("Requirements Installed")
            #         return True
            #     else:
            #         raise PyenvSetupException("ERROR INSTALLING PIP REQUIREMENTS :: FAILED TO INSTALL")
        except Exception as e:
            raise e