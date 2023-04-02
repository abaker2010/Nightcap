from nightcapcore.package import Package
from nightcapcore.command.command import Command
from nightcapcore.database.mongo.mongo_modules import MongoModuleDatabase
from nightcapcore.database.mongo.mongo_packages import MongoPackagesDatabase
from nightcapcore.database.mongo.mongo_submodules import MongoSubModuleDatabase

# Used to make sure that the package can be installed
#   IE: Not in the database(s)
class NightcapPackageDatabaseCheckCommand(Command):
    def __init__(self, package: Package = None) -> None:
        super().__init__()
        self.pkg:Package = package

    def execute(self) -> bool:
        _module = False
        _submodule = False

        # checking / preparing the Module
        try:
            MongoModuleDatabase().module_install(
                self.pkg.package_for.module
            )
            _module = True
        except Exception as e:
            raise e

        # checking / preparing the Submodule
        try:
            MongoSubModuleDatabase().submodule_install(
                self.pkg.package_for.module,
                self.pkg.package_for.submodule 
            )
            _submodule = True
        except Exception as e:
            raise e


        try:
            _package = MongoPackagesDatabase().installable(self.pkg)
        except Exception as e:
            raise e

        return (_module and _submodule and _package)

