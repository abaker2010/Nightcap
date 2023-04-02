
# region Imports
from typing import List
from nightcapcore.package.package import Package
from nightcapcore.database.mongo.mongo_printer import NightcapDatabsePrinter
# endregion

class NightcapOptionGenerator(object):
    """

    This class is used to help validate user input to the console

    ...

    Attributes
    ----------
        selectedList: -> list:
            Used for the current path of the program

        printer: -> Printer
            Allows access to the console printer


    Methods
    -------
        Accessible
        -------
            completed_options(self): -> list
                Tab auto complete for the options at the current path

            options(self, isDetailed=False): -> None
                This is used to select an option or to get the list of options that are available to be used

            option_help(self): -> None
                Override for the options help


        None Accessible
        -------

    """
    # region Init
    def __init__(self, selectedList: List[str] = None, package: Package = None) -> None:
        super().__init__()
        self.selectedList = selectedList
        self.package = package
        self.db_printer = NightcapDatabsePrinter()

    # endregion

    # region Options
    def options(self, isDetailed: bool = False, isParam: bool = False) -> None:
        if not isParam:
            if len(self.selectedList) == 0:
                self.db_printer.print_modules(isDetailed)
            elif len(self.selectedList) == 1:
                self.db_printer.print_submoduels(self.selectedList[0], isDetailed)
            elif len(self.selectedList) == 2:
                self.db_printer.print_packages(self.selectedList[0], self.selectedList[1], isDetailed)
            else:
                pass
        elif isParam:
            self.db_printer.print_package_params(self.package, isDetailed)
    # endregion

    # region Options Help
    def option_help(self) -> None:
        print(
            """
        Modules that are available to use to investigate pcap files.
        View modules using the 'options' command
            Optional detailed view with command: options detailed
        
            ~ Usage: use [module]
        """
        )
    # endregion