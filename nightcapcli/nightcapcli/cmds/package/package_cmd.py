# region Imports
import traceback
from typing import List
from colorama import Fore
from nightcapcore.package.filters.return_filters import ReturnFilters
from nightcapcore.package.filters.base import Filter
from nightcapcore.printers import Printer
from nightcapcore.invoker.invoker import Invoker
from nightcapcore.package.package import Package
from nightcapcli.base.base_cmd import NightcapBaseCMD
from nightcapcli.generator.option_generator import NightcapOptionGenerator
from nightcapcli.mixins.cmd_parts.options_cmdpart import OptionsCMDPart
from nightcapcli.mixins.cmd_parts.shell_cmdpart import ShellCMDPart
from nightcapcli.mixins.cmd_parts.projects_cmdpart import ProjectsCMDPart

from nightcapcore.reporting.report_data import ReportData
from nightcapcore.database.mongo.mongo_packages import MongoPackagesDatabase
from nightcapcore.reporting.commands.reporting_command import ReportingCommand
from nightcapcore.package.commands import PackageExecuteCommand, PackageFilterDataCommand
# endregion

class NightcapCLIPackageCMD(NightcapBaseCMD, OptionsCMDPart, ProjectsCMDPart, ShellCMDPart):
    """
    (User CLI Object)

    This class is used for the packages cli. IE: [<T>][<T>][<T>]

    ...

    Attributes
    ----------
        

        db: -> MongoPackagesDatabase
            Returns an instance of the MongoPackagesDatabase

        package_params: -> dict
            The package parameters for the currently selected package

    Methods
    -------
        Accessible
        -------
            do_projects(self, line): -> None:
                Enters into the projects cmd

            help_run(self, line): -> None
                Override for the runs help command

            do_run(self, line): -> None
                Allows the user to run the selected package

            do_update(self, line): -> None
                Trys to update, currently not working and looks like wrong place for the code
    """

    # region Init
    def __init__(
        self,
        selectedList: list,
        pkg: Package,
        channelid: str = "",
    ) -> None:

        NightcapBaseCMD.__init__(self, selectedList, channelid=channelid)
        OptionsCMDPart.__init__(self)
        ShellCMDPart.__init__(self)
        ProjectsCMDPart.__init__(self)
        self.pkg = pkg
        self.db = MongoPackagesDatabase()
        self.generatePcaps = True
        self.printer = Printer()

    # endregion

    def do_exit(self, line) -> bool:
        self.printer.debug("Selected list passed to package", self.selectedList)
        return super().do_exit(line)

    # region Help params
    def help_options(self) -> None:
        self.printer.item_2(
            "see parameters",
            "params",
            leadingTab=1,
            vtabs=1,
            leadingText="",
            textColor=Fore.LIGHTGREEN_EX,
        )
        self.printer.item_2(
            "set parameters",
            "params [PARAM] [PARAMVALUE]",
            leadingTab=1,
            endingBreaks=1,
            leadingText="",
            textColor=Fore.LIGHTGREEN_EX,
        )
    # endregion

    # region Do params
    def do_options(self, line) -> None:
        try:
            if line == "":
                NightcapOptionGenerator(package=self.pkg).options(isParam=True)
            elif line == "-d":
                NightcapOptionGenerator(package=self.pkg).options(isDetailed=True, isParam=True)
            else:
                print("Error with command")
        except Exception as e:
            self.printer.print_error(e)
    # endregion

    # region Help Run
    def help_run(self):
        self.printer.item_2(
            "Run package",
            leadingTab=1,
            vtabs=1,
            endingBreaks=1,
            leadingText="",
            textColor=Fore.LIGHTGREEN_EX,
        )

    # endregion

    # region Do Run
    def do_run(self, line) -> None:
        try:
            if self._check_params():
                _pkg_invoker = Invoker()
                _filter_invoker = Invoker()
                _report_invoker = Invoker()

                _hasProject = False

                if self.conf.project == None: 
                    self.printer.print_error("No project selected, no report data will be saved")
                    _hasProject = self.printer.input("Would you like to run without selecting a project? (y/N)")
                else:
                    _hasProject = True

                if _hasProject:
                    _pkg_invoker.set_on_start(PackageExecuteCommand(self.pkg, self.db))
                    _returned_data = _pkg_invoker.execute() 
                    if self.conf.project != None:
                        self.printer.print_formatted_additional("Return filters :: %s" % (self.pkg.package_information.return_filters))
                        _return_filters:ReturnFilters = None
                        if self.pkg.package_information.return_filters == None:
                            _general_filter =  { '0' : {
                                        "cid": 1,
                                        "name": "All Data",
                                        "replace": None,
                                        "replace_with": None,
                                        "replace_on_save": None,
                                        "replace_on_save_with": None,
                                        "regex": [
                                        "^.*?$",
                                        ],
                                        "sid": 0
                                    }}
                            
                            _return_filters = ReturnFilters({key: Filter(**value) for (key, value) in _general_filter.items()})
                        else:
                            _return_filters = self.pkg.package_information.return_filters

                        if _returned_data != {} and _returned_data != None:
                            # _filter_invoker.set_on_start(PackageFilterDataCommand(_returned_data, self.pkg.package_information.return_filters))
                            _filter_invoker.set_on_start(PackageFilterDataCommand(_returned_data, _return_filters))
                            _returned_data = _filter_invoker.execute()

                            if _returned_data != {} and _returned_data != None:
                                try:
                                    self.printer.print_formatted_check(f"Return data available :: {len(_returned_data)}", leadingBreaks=1, leadingTab=1)
                                    _report_invoker.set_on_start(ReportingCommand(self.conf.project, self.pkg.package_information, ReportData(_returned_data), self.pkg.report_design))
                                    _report_invoker.execute()
                                except Exception as e:
                                    print(traceback.print_exc())
                                    raise e
                            else:
                                self.printer.item_1("No return data available")
                else:
                    self.printer.print_error("Canceled execution")
                print()
        except Exception as e:
            self.printer.print_error("ERROR RUNNING PACKAGE :: %s" % e)
    # endregion

    # region Set Param
    def help_set(self) -> None:
        self.printer.item_2(
            "set default parameter",
            "set [PARAM] [DEFAULT VALUE]",
            leadingTab=1,
            vtabs=1,
            leadingText="",
            endingBreaks=1,
            textColor=Fore.LIGHTGREEN_EX,
        )
    # endregion

    # region Do Set Param
    def do_set(self, line, isDefault=False) -> bool:
        try:
            self.printer.debug("Pacakge Param Set")
            _split = line.split(" ")
            for k,v in self.pkg.package_information.entry_file_optional_params.items():
                if v.name == str(_split[0]):
                    v.value = str(_split[1])
            if isDefault:
                return True
        except Exception as se:
            self.printer.print_error(se)
            if isDefault:
                return False
    # endregion

    # region Complete Set
    def complete_set(self, text, line, begidx, endidx) -> List[str]:
        _ = [v.name for (k,v) in self.pkg.package_information.entry_file_optional_params.items()]
        return [i for i in _ if i.startswith(text)]
    # endregion

    # region Set Default
    def help_default(self) -> None:
        self.printer.item_2(
            "default parameter",
            "default [PARAM] [DEFAULT VALUE]",
            leadingTab=1,
            vtabs=1,
            leadingText="",
            endingBreaks=1,
            textColor=Fore.LIGHTGREEN_EX,
        )
    # endregion

    # region Do Set Param
    def do_default(self, line) -> None:
        try:
            if self.do_set(line, isDefault=True):
                self.printer.debug("Pacakge Param Set")
            else:
                self.printer.debug("ERROR :: Setting Package Param")

            if self.db.set_default_package_params(self.pkg):
                self.printer.debug("Pacakge Param default")
            else:
                self.printer.debug("ERROR :: Default Package Param")
        except Exception as se:
            self.printer.print_error(se)
    # endregion
    
    # region Complete Default
    def complete_default(self, text, line, begidx, endidx) -> List[str]:
        _ = [v.name for (k,v) in self.pkg.package_information.entry_file_optional_params.items()]
        return [i for i in _ if i.startswith(text)]
    # endregion

    def _check_params(self):
        for k, v in self.pkg.package_information.entry_file_optional_params.items():
            if bool(v.required):
                if v.value == "None":
                    raise Exception("Required param: %s" % (v.name))
        return True

    # region Override for Postloop for correcting navigation
    def postloop(self) -> bool:
        super().postloop()
        return True
    # endregion

    # region To JSON
    def toJson(self) -> dict:

        js = {
            "project": None
        }
        return js
    # endregion