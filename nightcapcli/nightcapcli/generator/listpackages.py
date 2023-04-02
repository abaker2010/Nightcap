
# region Imports
from nightcapcore import Package, Printer
from nightcapcore.printers.subprinters.schemas.default_schema import TableDefaultSchema
from nightcapcore.database.mongo.mongo_packages import MongoPackagesDatabase
# endregion

class NightcapListPackages(object):
    """

    This class is used to print the installed packages

    ...

    Attributes
    ----------
        packages_db: -> MongoPackagesDatabase
            Allows access to the MongoPackagesDatabase

        priner: -> Printer
            Allows access to the console printer


    Methods
    -------
        Accessible
        -------
            list_packages(self): -> None
                Prints the installed packages to the user

    """

    # region Init
    def __init__(self) -> None:
        super().__init__()
        self.packages_db = MongoPackagesDatabase()
        self.printer = Printer()
    # endregion

    # region List Packages
    def list_packages(self) -> None:
        _packages = list(map(lambda v: Package(v), self.packages_db.get_all_packages()))
        if _packages == []:
            self.printer.print_error(Exception("No Packages Installed"))
        else:
            _tdata = {
                        "Path" : [],
                        "Version" : [],
                        "Author" : [],
                        "Details" : []
                    }
            
            for pkg in _packages:
                _path = f"{pkg.package_for.module}/{pkg.package_for.submodule}/{pkg.package_information.package_name}"
                _author = f"{pkg.author.first_name} {pkg.author.last_name}"
                _tdata['Path'].append(_path)
                _tdata['Version'].append(str(pkg.package_information.version))
                _tdata['Author'].append(str(_author))
                _tdata['Details'].append(str(pkg.package_information.details))

            self.printer.table(title="Installed Packages", data=_tdata, newlines_before_table=0, schema=TableDefaultSchema(column_count=4, left_tindent=1))
    # endregion