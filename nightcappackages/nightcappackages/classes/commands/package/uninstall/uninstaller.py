# region Imports
import os
import glob
import shutil
from colorama import Fore
from nightcapcore import Printer
from nightcapcore.environment_support.golang.goenv_checks import GoenvChecks
from nightcapcore.environment_support.golang.goenv_delete import GoenvDeleteCommand
from nightcapcore.invoker import Invoker
from nightcapcore.package import Package
from nightcapcore.command.command import Command
from nightcapcore.environment_support import PyenvChecks
from nightcapcore.lang_supported.enum.lang_enum import LangEnum
from nightcapcore.environment_support.python.pyenv_delete import PyenvDeleteCommand
from nightcappackages.classes.paths import NightcapPackagesPaths, NightcapPackagesPathsEnum
from nightcapcore.database.mongo.mongo_modules import MongoModuleDatabase
from nightcapcore.database.mongo.mongo_packages import MongoPackagesDatabase
from nightcapcore.database.mongo.mongo_submodules import MongoSubModuleDatabase
# endregion

class NightcapPackageUninstallerCommand(Command):
    """

    This class is used to uninstall packages

    ...

    Attributes
    ----------
        printer: -> Printer
            allows us to print to the console

        _db: -> MongoPackagesDatabase
            allows us to remove the entry for the package from the database

    Methods
    -------
        Accessible
        -------
            execute(self): -> None
                run uninstall commands



        None Accessible
        -------
            _confim_delete(self, package_path: str): -> None
                Confirms deletion

            _delete(self, pkt: dict): -> None
                tries to uninstalls the package

    """

    # region Init
    def __init__(self, package_path: str, override: bool = False) -> None:
        self.printer = Printer()
        self._package_path = package_path
        self._db = MongoPackagesDatabase()
        self._override = override

    # endregion

    # region Execute
    def execute(self) -> None:
        try:
            if self._db.check_package_path(self._package_path.split("/")) == False:
                raise Exception("Package does not exist")
            else:

                _package = Package(MongoPackagesDatabase().get_package_config(
                        self._package_path.split("/")
                    ))
                    
                if self._override:
                    uconfirm = True
                else:
                    uconfirm = self._confim_delete(self._package_path)
                if uconfirm:
                    self.printer.print_header_w_option(
                        "Trying to Uninstall", self._package_path
                    )

                    self.printer.item_1(
                        "ID", str(_package.id), leadingText="[~]", seperator=" : "
                    )

                    # region Removing Package
                    try:
                        # region Deleting Package from DB
                        self._db.prackage_try_uninstall(_package) #delete(_package.id)
                        # endregion

                        # region Deleteing Files
                        self._delete(_package)
                        # endregion

                        # region Removing Submodules
                        MongoSubModuleDatabase().submodule_try_uninstall(
                            _package.package_for.module,_package.package_for.submodule
                        )
                        # endregion

                        # region Removing Modules
                        if (
                            len(MongoSubModuleDatabase()
                            .find_submodules(_package.package_for.module))
                            == 0
                        ):
                            MongoModuleDatabase().module_try_unintall(
                                _package.package_for.module
                            )
                        # endregion


                        self._rm_installer(_package)
                    except Exception as e:
                        raise e
                    # endregion

                    # region Cleaning Up Virtenv
                    if str(_package.package_information.language.language).lower() == str(LangEnum.PYTHON):
                        if PyenvChecks().check_env(_package.package_information.language.env_name):
                            try:
                                _pyenv_invoker = Invoker()
                                _pyenv_invoker.set_on_start(PyenvDeleteCommand(_package.package_information.language))
                                _pyenv_invoker.execute()
                            except Exception as e:
                                self.printer.print_error(f"ERROR REMOVING PYENV :: {e}")
                    elif str(_package.package_information.language.language).lower() == str(LangEnum.GO):
                        # if GoenvChecks().check_env(_package.package_information.entry_file):
                        try:
                            _goenv_invoker = Invoker()
                            _goenv_invoker.set_on_start(GoenvDeleteCommand(_package.package_information))
                            _goenv_invoker.execute()
                        except Exception as e:
                            self.printer.print_error(f"ERROR REMOVING GOENV :: {e}")
                            
                        self.printer.print_formatted_additional("GOENV CLEANED UP")
                    else:
                        self.printer.print_formatted_additional("NO VIRTENV TO CLEAN UP")

                    # endregion
                else:
                    raise Exception("User Cancled Uninstall")
            self.printer.print_formatted_check(
                text="UNINSTALLED",
                vtabs=1,
                endingBreaks=1,
                leadingTab=1,
            )
            return True

        except Exception as e:
            raise e

    # endregion

    # region Copy
    def _rm_installer(self, pkg: Package):
        _path = NightcapPackagesPaths().generate_path(
            NightcapPackagesPathsEnum.Installers,
            ["-".join([pkg.package_for.module, pkg.package_for.submodule, pkg.package_information.package_name, "*"])],
        )

        _files = glob.glob(_path)
        for f in _files:
            try:
                os.remove(f)
            except Exception as e:
                self.printer.print_error(e)

    # endregion

    # region Confirm Delete
    def _confim_delete(self, package_path: str):
        return self.printer.input(
            "Are you sure you want to uninstall? [y/N]: ", questionColor=Fore.RED
        )

    # endregion

    # region Delete
    def _delete(self, pkg: Package):
        _path = NightcapPackagesPaths().generate_path(
            NightcapPackagesPathsEnum.PackagesBase,
            [
                pkg.package_for.module,
                pkg.package_for.submodule,
                pkg.package_information.package_name
            ],
        )
        try:
            shutil.rmtree(_path)
            self.printer.print_formatted_check(text="Deleted Files")
        except OSError as e:
            self.printer.print_error(
                Exception("Error: %s - %s." % (e.filename, e.strerror))
            )

    # endregion
