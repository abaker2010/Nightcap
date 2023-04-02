# region Imports
import traceback
from colorama import Fore
from nightcapcore import Printer, ScreenHelper
from nightcapcore.invoker import Invoker
from nightcapcore.package import Package
from nightcapcore.command.command import Command
from nightcapcore.helpers.tmp_files import NightcapTmpFiles
from nightcapcore.lang_supported.enum.lang_enum import LangEnum
from nightcappackages.classes.commands.package.uninstall.uninstaller import NightcapPackageUninstallerCommand


from .environment import NightcapPackageInstallPyenvPythonCommand, NightcapPackageInstallerGoenvCommand
from ..backup import NightcapPackageNCPBackupCommand
from ..packing import NightcapPackageUnpackerCommand
from .custom import NightcapCustomPackageInstallerCommand
from .github import NightcapGithubPackageInstallerCommand
from nightcappackages.classes.paths import NightcapPackagesPaths
from nightcappackages.classes.commands.database import NightcapPackageDatabaseCheckCommand, NightcapPackageDatabaseUninstallCommand
from nightcapcore.exceptions.virtenv.setup import EnvSetupException
from nightcapcore.exceptions.github import GithubException
from nightcapcore.exceptions.database import DatabaseAlreadyInstallException
# endregion

class NightcapPackageInstallerCommand(Command):
    """

    This class is used to install packages

    ...

    Attributes
    ----------
        _package_paths: -> NightcapPackagesPaths
            used for package installation path

        _db: -> MongoPackagesDatabase
            for an instance to the MongoDB database

        _printer: -> Printer
            allows us to print to the console

        _package: -> dict
            the package information that will be used to be installed


    Methods
    -------
        Accessible
        -------
            execute(self) -> None:
                executes the installer

        None Accessible
        -------
            _copy(self, pkt: dict, src: str): -> None
                copies data to the the needed locations

            _imports(self, package: dict = None): -> bool
                gets needed imports for the programs

            _install_import(self, imprt: dict = None, reinstall: bool = False): -> bool
                installs the collected imports
    """

    # region Init
    def __init__(self, package_path: str) -> None:
        self.tmp_folder = NightcapTmpFiles()
        self.printer = Printer()
        self._package_path = package_path
        self._package_paths = NightcapPackagesPaths()
        self._pkg:Package = None
    # endregion

    # region Execute
    def execute(self) -> None:
        ScreenHelper().clearScr()
        self.printer.print_underlined_header_undecorated("Starting Install")
        _failed:bool = False
        try:
            self.printer.print_underlined_header("Create Tmp Folder")
            _tmp = self.tmp_folder.create_folder()
            self.printer.print_formatted_additional("Tmp Path", _tmp)

            _invoker_dbprepare = Invoker()
            _invoker_unpack = Invoker()
            _invoker_backupncp = Invoker()
            _invoker_requirements = Invoker()
            
            #region Backing Up NCP
            _invoker_backupncp.set_on_start(NightcapPackageNCPBackupCommand(self._package_path))
            _invoker_backupncp.execute()
            #endregion 

            #region Unpack NCP
            _invoker_unpack.set_on_start(NightcapPackageUnpackerCommand(self._package_path, _tmp))
            self._pkg:Package = _invoker_unpack.execute()
            #endregion

            #region Prepare Database
            _invoker_dbprepare.set_on_start(NightcapPackageDatabaseCheckCommand(self._pkg))
            _db_ready:bool = _invoker_dbprepare.execute()
            #endregion

            #region Install Package Custom/Github
            _installed:bool = False
            if _db_ready == True:
                invoker = Invoker()
                if self._pkg.package_information.github.url != None:
                    invoker.set_on_start(
                        NightcapGithubPackageInstallerCommand(self._pkg)
                    )
                else:
                    invoker.set_on_start(
                        NightcapCustomPackageInstallerCommand(
                            self._pkg,
                            self._package_path
                        )
                    )
                _installed:bool = invoker.execute()
            else:
                raise Exception("ERROR PREPARING DATABASE :: FAILED TO INSTALL")

            try:
                if _installed:
                    if str(self._pkg.package_information.language.language).lower() == str(LangEnum.PYTHON):
                        _invoker_requirements.set_on_start(NightcapPackageInstallPyenvPythonCommand(self._pkg))
                        _requirements_installed:bool = _invoker_requirements.execute()
                        if _requirements_installed:
                            self.printer.print_formatted_check("NCP Requirements Installed (Python)")
                        else:
                            raise Exception("ERROR INSTALLING NCP REQUIREMENTS (Python)")
                    elif str(self._pkg.package_information.language.language).lower() == str(LangEnum.GO):  
                        _invoker_requirements.set_on_start(NightcapPackageInstallerGoenvCommand(self._pkg))
                        _requirements_installed:bool = _invoker_requirements.execute()
                        if _requirements_installed:
                            self.printer.print_formatted_check("NCP Requirements Installed (Go)")
                        else:
                            raise Exception("ERROR INSTALLING NCP REQUIREMENTS (Go)")
                    else: 
                        raise Exception("ERROR LANGUAGE INSTALLER COMMAND NOT FOUND %s" % (str(self._pkg.package_information.language.language)))
            except Exception as e:
                invoker = Invoker()
                invoker.set_on_start(NightcapPackageDatabaseUninstallCommand(self._pkg))
                invoker.execute()
                raise e
            #endregion
        except DatabaseAlreadyInstallException as db_error:
            self.printer.print_error(db_error)
            _failed = True
        except (EnvSetupException, GithubException) as setup_error:
            _failed = True
            self.printer.print_error(f"{'GITHUB EXCEPTION' if type(setup_error) == GithubException else 'PYENV EXCEPTION'} :: {setup_error}")
            try:
                _remove_pkg_invoker = Invoker()
                _pkg_path = f"{self._pkg.package_for.module}/{self._pkg.package_for.submodule}/{self._pkg.package_information.package_name}"
                _remove_pkg_invoker.set_on_start(NightcapPackageUninstallerCommand(_pkg_path, override=True))
                _removed = _remove_pkg_invoker.execute()
                if _removed:
                    self.printer.print_error(Exception(f"REMOVED FAILED INSTALLATION FROM DB"))
            except Exception as e:
                raise e
        except Exception as e:
            self.printer.print_error(e)
            _failed = True
        finally:
            self.tmp_folder.clean_up()
            if _failed == False:
                self.printer.print_formatted_check("Install Done", leadingBreaks=1,endingBreaks=1, leadingTab=1)

    # endregion
