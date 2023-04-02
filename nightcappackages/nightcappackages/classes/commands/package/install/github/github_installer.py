# region Imports
from nightcapcore import Printer
from nightcapcore.invoker import Invoker
from nightcapcore.package import Package
from nightcapcore.command.command import Command
from nightcapcore.exceptions.github.clone import GithubCloneException
from nightcappackages.classes.paths.paths import NightcapPackagesPaths
from nightcappackages.classes.paths.pathsenum import NightcapPackagesPathsEnum
from nightcappackages.classes.commands.package.git import NightcapPackageGitCloneCommand
# endregion

class NightcapGithubPackageInstallerCommand(Command):
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

    # region Execute
    def execute(self) -> None:
        try:
            self.printer.print_underlined_header("Cloning Git Repo")
            invoker = Invoker()
            invoker.set_on_start(
                NightcapPackageGitCloneCommand(
                    self.package.package_information.github.url, self.package_install_location, self.package.package_information.github.commit_id
                )
            )
            _installed = invoker.execute()

            if _installed:
                self.printer.print_formatted_check("Cloned")
                return True
            else:
                raise GithubCloneException("ERROR FAILED TO CLONE REPO")

        except Exception as e:
            raise GithubCloneException(f"ERROR CLONING GITHUB REPO :: {e}")
    # endregion