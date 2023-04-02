# region Imports
import os
import shutil
from nightcapcore import Printer, Command
from nightcappackages.classes.paths.paths import NightcapPackagesPaths
from nightcappackages.classes.paths.pathsenum import NightcapPackagesPathsEnum
# endregion

class NightcapPackageNCPBackupCommand(Command):
    # region Init
    def __init__(
        self,
        ncp_path: str,
        verbose: bool = False,
    ):
        self.printer = Printer()
        self.verbose = verbose
        self.ncp_path = ncp_path
        self.installers_backup_loation = NightcapPackagesPaths().generate_path(
            NightcapPackagesPathsEnum.Installers
        )
    # endregion
    
    # region Backup Installer
    def _backup_installer(self, file: str = None):
        try:
            
            if os.path.exists(
                os.path.join(self.installers_backup_loation, file)
            ):
                os.remove(os.path.join(self.installers_backup_loation, file))

            shutil.copy(self.ncp_path, self.installers_backup_loation)
            
            return True
        except OSError as e:
            raise Exception("Package not copied (.ncp) Error: %s" % str(e))
    # endregion

    def execute(self) -> None:

        try:
            _filename = os.path.basename(self.ncp_path)
            self.printer.print_underlined_header("Backup NCP File")
            self.printer.print_formatted_additional("NCP File", _filename)
            _backed_up = self._backup_installer(_filename)

            if _backed_up:
                self.printer.print_formatted_check("NCP Backed Up")
                return True 
            else:
                raise Exception("ERROR BACKING UP NCP")
        except Exception as e:
            self.printer.print_error(e)
            raise e
