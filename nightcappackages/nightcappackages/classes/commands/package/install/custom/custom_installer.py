# region Imports
import errno
import shutil
from nightcapcore.printers import Printer
from nightcapcore.package import Package
from nightcapcore.command.command import Command
from nightcappackages.classes.paths import NightcapPackagesPaths
from nightcappackages.classes.paths.paths import NightcapPackagesPaths
from nightcappackages.classes.paths.pathsenum import NightcapPackagesPathsEnum
# endregion

class NightcapCustomPackageInstallerCommand(Command):
    def __init__(self, package: Package, unpacked_path: str) -> None:
        super().__init__()
        self.printer = Printer()
        self.package:Package = package
        self.unpacked_path = unpacked_path

        self.package_install_location = NightcapPackagesPaths().generate_path(
            NightcapPackagesPathsEnum.PackagesBase,
            [
                self.package.package_for.module,
                self.package.package_for.submodule, 
                self.package.package_information.package_name
            ],
        )

    # region Move Repo
    def _move_repo(self):
        try:
            shutil.move(self.unpacked_path, self.package_install_location)
            return True
        except OSError as e:
            # If the error was caused because the source wasn't a directory
            if e.errno == errno.ENOTDIR:
                shutil.move(self.unpacked_path, self.package_install_location)
                return True
            else:
                raise Exception("Package not copied. (Installer Files) Error: %s" % str(e))
    # endregion

    def execute(self) -> dict:
        try:
            if self._move_repo():
                self.printer.item_1("Installed Package", endingBreaks=1)
                return True
            else:
                raise Exception("ERROR INSTALLING CUSTOM PACKAGE :: FAILED")
        except Exception as e:
            raise e