from nightcapcore import Printer
from nightcapcore.package import Package
from nightcapcore.command.command import Command
from nightcapcore.database.mongo.mongo_packages import MongoPackagesDatabase

# Used to make sure that the package can be installed
#   IE: Not in the database(s)
class NightcapPackageDatabaseUninstallCommand(Command):
    def __init__(self, package: Package = None) -> None:
        super().__init__()
        self.pkg:Package = package
        self.printer = Printer()

    def execute(self) -> bool:
        try:
            _package = MongoPackagesDatabase().get_package_config(
                    [self.pkg.package_for.module, self.pkg.package_for.submodule, self.pkg.package_information.package_name]
                )

            MongoPackagesDatabase().delete(_package['_id'])
            return True
        except Exception as e:
            raise e
            