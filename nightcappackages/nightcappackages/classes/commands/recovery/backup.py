# region Imports
import os
import json
import shutil
import tempfile
from datetime import datetime
from nightcapcore.command.command import Command
from nightcapcore.helpers import NightcapJSONEncoder
from nightcapcore.printers.print import Printer
from nightcappackages.classes.paths.paths import NightcapPackagesPaths
from nightcappackages.classes.paths.pathsenum import NightcapPackagesPathsEnum
from nightcapcore.database.mongo.mongo_modules import MongoModuleDatabase
from nightcapcore.database.mongo.mongo_packages import MongoPackagesDatabase
from nightcapcore.database.mongo.mongo_submodules import MongoSubModuleDatabase
# endregion

class NightcapBackupCommand(Command):
    def __init__(self, path: str) -> None:
        super().__init__()
        self.path = path
        self.printer = Printer()
        self._package_paths = NightcapPackagesPaths()

    def execute(self) -> None:
        if len(self.path) == 0:
            self.printer.print_error(Exception("Please enter an output location"))
        else:
            self.printer.print_underlined_header("Starting Backup")
            # self.printer.print_formatted_additional("Backup Location:", optionaltext=str(line))

            self.tmpdir = tempfile.mkdtemp()
            try:
                self.printer.print_formatted_additional(
                    "Tmp Location", optionaltext=self.tmpdir
                )

                self._backup_installers(self.tmpdir)
                self._backup_databases(self.tmpdir)

                self.printer.print_underlined_header("Moving Backup")
                now = datetime.now()
                # date and time format: dd/mm/YYYY H:M:S
                format = "%d-%m-%Y-%H-%M-%S"
                # format datetime using strftime()
                time1 = now.strftime(format)
                self._move_backup(self.tmpdir, str(self.path), "backup_" + str(time1))

                self.printer.print_formatted_additional(
                    "Backup Complete", endingBreaks=1, leadingTab=1, leadingBreaks=1
                )
            except Exception as e:
                    raise e
            finally:
                shutil.rmtree(self.tmpdir)

    def _move_backup(self, source, destination, name):
        try:
            self._make_archive(source, destination, name, "zip")
        except Exception as e:
            print("Error :: File already exists")
        os.rename(
            os.path.join(destination, name + ".zip"),
            os.path.join(destination, name + ".ncb"),
        )
        self.printer.print_formatted_check("Done", endingBreaks=1)

    def _backup_installers(self, output: str):
        _installer_path = self._package_paths.generate_path(
            NightcapPackagesPathsEnum.Installers
        )

        self.printer.print_underlined_header("Backing Up Installers")
        self.printer.print_formatted_additional(
            "Installer(s) Location: ", optionaltext=_installer_path
        )
        self.printer.print_formatted_additional("Backup Location:", optionaltext=output)

        self._make_archive(_installer_path, output, "installers", "zip")
        self.printer.print_formatted_check("Done")

    def _backup_databases(self, output: str):

        self.printer.print_underlined_header("Backing Up Collections")

        _packages = self._backup_packages()
        self._write_file(output, "packages.json", _packages)
        self.printer.print_formatted_additional("Packages", optionaltext="Backed Up")

        # _projects = self._backup_projects()
        # self._write_file(output, "projects.json", _projects)
        # self.printer.print_formatted_additional("Projects", optionaltext="Backed Up")

        _submodules = self._backup_submodules()
        self._write_file(output, "submodules.json", _submodules)
        self.printer.print_formatted_additional("Submodules", optionaltext="Backed Up")

        _modules = self._backup_modules()
        self._write_file(output, "modules.json", _modules)
        self.printer.print_formatted_additional("Modules", optionaltext="Backed Up")

        self.printer.print_formatted_check("Done")

    def _write_file(self, dest, name, data):
        _json_data = json.dumps(data, cls=NightcapJSONEncoder)
        with open(os.path.join(dest, name), "w") as outfile:
            outfile.write(_json_data)

    # region make archive(s)
    def _make_archive(self, source, destination, name, format):
        shutil.make_archive(name, format, source)
        shutil.move("%s.%s" % (name, format), destination)

    def _backup_modules(self):
        _modules = MongoModuleDatabase().read()
        return list(_modules)

    def _backup_submodules(self):
        _submodules = MongoSubModuleDatabase().read()
        return list(_submodules)

    def _backup_packages(self):
        _packages = MongoPackagesDatabase().read()
        return list(_packages)

    def _backup_projects(self):
        return list()

    # endregion