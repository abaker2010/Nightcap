import re
from typing import List, Dict, Tuple
from nightcapcore import Command, Printer
from nightcapcore.package.filters.base.filter import Filter
from nightcapcore.package.filters.return_filters import ReturnFilters

class PackageFilterDataCommand(Command):
    def __init__(self, returned_data: Tuple[str, List[str]], return_filters: Dict[str, Filter] = None):
        self.return_data:Tuple[str, List[str]] = returned_data
        self.return_filters:ReturnFilters = return_filters
        self.printer = Printer()

    def execute(self) -> dict:
        try:
            _reg_matched = []

            id:int = 0

            if self.return_filters != None:
                for filter_types, filter_values in self.return_filters.return_filters.items():
                    report_filter:Filter = filter_values

                    for data in self.return_data[1]:
                        for reg in report_filter.regex:
                            self.printer.debug("-" * 10)
                            self.printer.debug("Regex: %s" % (reg))
                            self.printer.debug("Before cleaning colors: %s" % (data))
                            ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
                            result = ansi_escape.sub('', data)
                            result = repr(result.strip())
                            self.printer.debug("After cleaning colors: %s" % (result))

                            if report_filter.replace != None and report_filter.replace_with != None:
                                result = str(result).replace(report_filter.replace, report_filter.replace_with)
                                self.printer.debug("Replacing data: %s with %s" % (report_filter.replace, report_filter.replace_with))
                                self.printer.debug("After Replace: %s" % (str(result)))
                            
                            _matched = re.match(reg, str(eval(result)))
                            if _matched != None:
                                self.printer.debug("Regex Matched String: %s" % (_matched))
                                result_forsave = _matched.string
                                if report_filter.replace_on_save != None and report_filter.replace_on_save_with != None:
                                    self.printer.debug("Before On Save: %s" % (result_forsave))
                                    result_forsave = str(result_forsave).replace(report_filter.replace_on_save, report_filter.replace_on_save_with)
                                    self.printer.debug("Replacing On Save: %s with %s" % (report_filter.replace_on_save, report_filter.replace_on_save_with))
                                    self.printer.debug("After Replace On Save : %s" % (str(result_forsave)))


                                _tmp = {"id" : id, "cid" : report_filter.cid, "name" : report_filter.name, "sid" : report_filter.sid, "value" : result_forsave}
                                if _tmp not in _reg_matched:
                                    _reg_matched.append(_tmp)
                                    id += 1
                            self.printer.debug("-"*10)

            return _reg_matched
        except Exception as e:
            raise e

            