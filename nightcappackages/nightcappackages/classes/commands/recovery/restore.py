# region Imports
import os
import shutil
import tempfile
from colorama import Fore, Style
from nightcapcore.printers.print import Printer
from nightcappackages.classes.helpers.clean import NightcapCleanHelper
from nightcappackages.classes.commands import NightcapPackageInstallerCommand
# endregion

class NightcapRestoreHelper(object):
    def __init__(self, path: str) -> None:
        super().__init__()
        self.path = path
        self.printer = Printer()

    def restore(self):
        if ".ncb" in str(self.path).split(os.sep)[-1]:

            self.printer.print_underlined_header("Starting Restore", leadingBreaks=1)
            self.printer.print_formatted_additional(
                "Restore File Path", optionaltext=self.path, endingBreaks=1
            )

            _cleaned = NightcapCleanHelper().clean()

            if _cleaned:
                self.printer.print_underlined_header("Unpacking Backup")
                self.tmpdir = tempfile.mkdtemp()

                shutil.copy(str(self.path), self.tmpdir)
                name = os.path.basename(str(self.path))
                new_name = name.replace(".ncb", ".zip")
                dir = os.path.dirname(str(self.path))

                os.rename(
                    os.path.join(self.tmpdir, name), os.path.join(self.tmpdir, new_name)
                )

                shutil.unpack_archive(
                    os.path.join(self.tmpdir, new_name),
                    os.path.join(self.tmpdir, "restoring_backup"),
                    "zip",
                )
                shutil.unpack_archive(
                    os.path.join(self.tmpdir, "restoring_backup", "installers.zip"),
                    os.path.join(self.tmpdir, "restoring_backup", "installers"),
                    "zip",
                )
                self.printer.print_formatted_check("Successfully unpacked backup")

                _installers_path = os.path.join(
                    self.tmpdir, "restoring_backup", "installers"
                )
                _r_paths = self._restore_installers_paths(_installers_path)
                for _r in _r_paths:
                    self._restore_installers(_r)
                    print(
                        "\n\t\t"
                        + Fore.LIGHTMAGENTA_EX
                        + "*" * 25
                        + Style.RESET_ALL
                        + "\n"
                    )

                self.printer.item_1("Cleaning Up", leadingBreaks=1, endingBreaks=1)
                shutil.rmtree(self.tmpdir)
                self.printer.print_formatted_check(
                    "Restore Completed", leadingBreaks=1, endingBreaks=1
                )
                return True
            else:
                self.printer.print_error(
                    Exception(
                        "There was an error when cleaning, please view above for more details."
                    )
                )
                return False
        else:
            self.printer.print_error(
                Exception("Please check the backup file. Inforrect file type used")
            )
            return False

    def _restore_installers_paths(self, location: str):
        _installers = []

        for root, dirs, files in os.walk(location):
            for file in files:
                if file.endswith(".ncp"):
                    # print(file)
                    _installers.append(
                        {
                            "name": file.replace(".ncp", ""),
                            "path": os.path.join(root, file),
                        }
                    )
        return _installers

    def _restore_installers(self, installers: str):
        _pack = NightcapPackageInstallerCommand(installers["path"])
        _pack.execute()
