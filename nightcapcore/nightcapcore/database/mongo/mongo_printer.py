import traceback
from typing import List
from colorama import Fore, Style

from nightcapcore.printers.print import Printer
from nightcapcore.package.package import Package
from nightcapcore.package.module.module import Module
from nightcapcore.package.submodule.submodule import Submodule
from nightcapcore.database.mongo.mongo_modules import MongoModuleDatabase
from nightcapcore.database.mongo.mongo_packages import MongoPackagesDatabase
from nightcapcore.database.mongo.mongo_submodules import MongoSubModuleDatabase
from nightcapcore.printers.subprinters.schemas.default_schema import TableDefaultSchema

class NightcapDatabsePrinter():
    def __init__(self) -> None:
        self._modules = MongoModuleDatabase()
        self._submodules = MongoSubModuleDatabase()
        self._packages = MongoPackagesDatabase()
        self.printer = Printer()

        self._detailed_format = "\t\t%s- %s%s  :  %s%s%s"
        self._normal_format = "%s %s(%s)%s"

        self._normal_package_format = "%s%s"
        self._detailed_package_format = "\t\t%s- %s%s  :  %s%s%s"
        
    def print_modules(self, isDetailed: bool = False):
        _moduels:List[Module] = self._modules.get_all_modules()
        if _moduels != []:
            if isDetailed == True:
                self.printer.print_header_w_option("Module Name", "(Submodule Count)")
                for module in _moduels:
                    _count = len(MongoSubModuleDatabase().find_submodules(module.type))
                    print(self._detailed_format % (Fore.LIGHTMAGENTA_EX, Fore.LIGHTGREEN_EX, module.type, Fore.LIGHTMAGENTA_EX, str(_count), Style.RESET_ALL))
                print("\n")
            else:
                _vals = []
                for module in _moduels:
                    _count = len(MongoSubModuleDatabase().find_submodules(module.type))
                    _vals.append(self._normal_format % (module.type, Fore.LIGHTMAGENTA_EX, str(_count), Style.RESET_ALL))
                self._print_dynamic(_vals)
        else:
            self.printer.print_error(Exception("No Modules Installed"))

    def print_submoduels(self, module: str, isDetailed: bool = False):
        _submodule:List[Submodule] = self._submodules.find_submodules(module)
        
        if _submodule != []:
            if isDetailed == True:
                self.printer.print_header_w_option("Submodule Name", "(Package Count)")
                for submodule in _submodule:
                    _count = MongoPackagesDatabase().find_packages(submodule.module, submodule.type).count()
                    print(self._detailed_format % (Fore.LIGHTMAGENTA_EX, Fore.LIGHTGREEN_EX, submodule.type, Fore.LIGHTMAGENTA_EX, str(_count), Style.RESET_ALL))
                print("\n")
            else:
                _vals = []
                for submodule in _submodule:
                    _count = MongoPackagesDatabase().find_packages(submodule.module, submodule.type).count()
                    _vals.append(self._normal_format % (submodule.type, Fore.LIGHTMAGENTA_EX, str(_count), Style.RESET_ALL))
                self._print_dynamic(_vals)
        else:
            self.printer.print_error(Exception("No Modules Installed"))

    def print_packages(self, module: str, submodule: str, isDetailed: bool = False):
        _packages:List[Package] = MongoPackagesDatabase().get_packages_list(module, submodule)
        if _packages != []:
            if isDetailed == True:
                self.printer.print_underlined_header("Package Name")
                for package in _packages:
                    print(self._detailed_format % (Fore.LIGHTMAGENTA_EX, Fore.LIGHTGREEN_EX, package.package_information.package_name, Fore.LIGHTMAGENTA_EX, str(package.author), Style.RESET_ALL))
                print("\n")
            else:
                _vals = []
                for package in _packages:
                    _vals.append(self._normal_package_format % (package.package_information.package_name, Style.RESET_ALL))
                self._print_dynamic(_vals)
        else:
            self.printer.print_error(Exception("No Packages Installed"))

    def print_package_params(self, package: Package, isDetailed: bool = False):
        if package.package_information.entry_file_optional_params != None:
            if isDetailed == False:
                self.printer.print_underlined_header("Package Parameters", endingBreaks=0)
            _tdata = {
                        "Param" : [],
                        "Value" : [],
                        "Required" : [],
                        "Details" : []
                    }

            for k, v in package.package_information.entry_file_optional_params.items():
                    if isDetailed == False:
                        
                        self.printer.print_formatted_other(
                                "%s%s"
                                % (
                                    "(Required) "
                                    if v.required == True
                                    else "",
                                    str(v.name).upper(),
                                ),
                                str(v.value),
                                leadingTab=3,
                                optionalTextColor=Fore.YELLOW,
                            )
                    else:
                        _param = f"{str(v.name).upper()}"
                        _value = str(v.value)
                        _details = str(v.description)

                        _tdata['Param'].append(_param)
                        _tdata['Value'].append(_value)
                        _tdata['Required'].append(str(v.required))
                        _tdata['Details'].append(_details)
            
            if isDetailed:
                try:
                    self.printer.table(title="Package Parameters", data=_tdata, schema=TableDefaultSchema(column_count=4), newlines_before_table=0)
                except Exception as e:
                    self.printer.print_error(e)
                    print(traceback.print_exc())
                        
            print("\n")
        else:
            print(Fore.LIGHTGREEN_EX + "\t\tPackage Parameters" + Style.RESET_ALL)

    def _print_dynamic(self, vals: list):
        _cvals = []
        _join = Fore.YELLOW + " | " + Style.RESET_ALL
        vals = list(map(lambda v: Fore.CYAN + v + Style.RESET_ALL, vals))

        if len(vals) != 0:
            if len(vals) > 1:
                for v in vals:
                    _cvals.append(v)
                    _cvals.append(_join)
                _cvals = _cvals[:-1]
            else:
                for v in vals:
                    _cvals.append(v)

        self.printer.item_1(
                "".join(_cvals),
                "",
                leadingTab=1,
                leadingText="",
                vtabs=1,
                endingBreaks=1,
                seperator="",
            )
