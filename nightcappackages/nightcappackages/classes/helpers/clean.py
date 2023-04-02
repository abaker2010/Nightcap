import shutil
import os
from nightcapcore.printers.print import Printer
from nightcappackages.classes.paths.paths import NightcapPackagesPaths
from nightcappackages.classes.paths.pathsenum import NightcapPackagesPathsEnum
from nightcapcore.database.mongo.mongo_modules import MongoModuleDatabase
from nightcapcore.database.mongo.mongo_packages import MongoPackagesDatabase
from nightcapcore.database.mongo.mongo_submodules import MongoSubModuleDatabase


class NightcapCleanHelper(object):
    def __init__(self) -> None:
        super().__init__()
        self.printer = Printer()
        self._package_paths = NightcapPackagesPaths()

    def clean(self):
        _cleaned = self._clean_all()

        if _cleaned:
            self.printer.print_formatted_check(
                "Cleaning was successful", leadingBreaks=1, endingBreaks=1, leadingTab=1
            )
        else:
            self.printer.print_error(
                Exception(
                    "There was an error when cleaning, please view above for more details."
                )
            )

        return _cleaned

    def _clean_all(self):
        self.printer.print_underlined_header("Cleaning")

        _installer_path = self._package_paths.generate_path(
            NightcapPackagesPathsEnum.Installers
        )

        _packages_path = self._package_paths.generate_path(
            NightcapPackagesPathsEnum.PackagesBase
        )

        _passed = True

        try:
            shutil.rmtree(_installer_path)
            self.printer.print_formatted_check("Cleaned", optionaltext=("Installers"))
        except Exception as e:
            self.printer.print_formatted_additional(
                "Installers Not Cleaned", optionaltext=str(e)
            )
            _passed = False

        try:
            os.makedirs(_installer_path)
            self.printer.print_formatted_check(
                "Created", optionaltext=("Installers Location")
            )
        except Exception as e:
            self.printer.print_formatted_additional(
                "Installers Not Created", optionaltext=str(e)
            )
            _passed = False

        try:
            shutil.rmtree(_packages_path)
            self.printer.print_formatted_check(
                "Cleaned", optionaltext=("Packages"), leadingBreaks=1
            )
        except Exception as e:
            self.printer.print_formatted_additional(
                "Installers Not Cleaned", optionaltext=str(e)
            )
            _passed = False

        try:
            os.makedirs(_packages_path)
            self.printer.print_formatted_check(
                "Created", optionaltext=("Packages Location")
            )
        except Exception as e:
            self.printer.print_formatted_additional(
                "Installers Not Created", optionaltext=str(e)
            )
            _passed = False

        try:
            self._drop_dbs()
            self.printer.print_formatted_check("Database", optionaltext=("Successful"))
        except Exception as e:
            self.printer.print_formatted_additional(
                "Dropping DB's", optionaltext=str(e)
            )
            _passed = False

        return _passed

    def _drop_dbs(self):
        try:
            MongoModuleDatabase().drop()
        except Exception as e:
            self.printer.print_error(e)

        try:
            MongoSubModuleDatabase().drop()
        except Exception as e:
            self.printer.print_error(e)

        try:
            MongoPackagesDatabase().drop()
        except Exception as e:
            self.printer.print_error(e)
