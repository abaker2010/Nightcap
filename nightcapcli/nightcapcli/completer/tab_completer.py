
# region Imports
import re
from typing import List
from nightcapcore.package.module.module import Module
from nightcapcore.package.submodule.submodule import Submodule
from nightcapcore.database.mongo.mongo_modules import MongoModuleDatabase
from nightcapcore.database.mongo.mongo_packages import MongoPackagesDatabase
from nightcapcore.database.mongo.mongo_submodules import MongoSubModuleDatabase
from nightcapcore.singleton.singleton import Singleton
# endregion

class NightcapTabCompleter(object, metaclass=Singleton):

    def __init__(self) -> None:
        super().__init__()
        self.modules = []
        self.submodules = {}
        self.packages = {}

    def _clean_options(self, data: List[str], text: str, error: str) -> List[str]:
        _vals = []
        if text == "":
            if len(data) != 0:
                if hasattr(data[0], 'type'):
                    _vals = list(map(lambda x: x.type, data))
                else:
                    _vals = list(map(lambda x: x, data))
        else:
            if len(data) != 0:
                if hasattr(data[0], 'type'):
                    _vals = [i for i in list(map(lambda x: x.type, data)) if str(i).startswith(text)]
                else:
                    _vals = [i for i in list(map(lambda x: x, data)) if i.startswith(text)]


        if _vals == []:
            return [("No %s Installed" % (error)), " "]
        else:
            return _vals

    # region Caching
    def _check_cached(self):
        # return None or the list of modules
        pass

    def _check_db(self):
        # return the information from the db after caching
        pass

    def _get_modules(self) -> List[Module]:
        _ = MongoModuleDatabase().get_all_modules()
        return _

    def _get_submodules(self, module: str) -> List[Submodule]:
        _ = MongoSubModuleDatabase().find_submodules(module)
        return _

    def _get_packages(self, module: str, submodule: str) -> List:
        _ = MongoPackagesDatabase().packages([module, submodule], False)
        return _
    # endregion

    def complete(self, selected: List[str], text: str, line: str) -> List[str]:
        try:
            _re_line = re.match("^(.*?)(?:(?:\/(.*?)(?:\/(.*?)|$)|$)|$)$", line)
            _groups = _re_line.groups()
            _split_count = line.count('/') 

            _new = [i for i in _groups if i != None and i != '']
            _new = selected + _new
            
            if len(selected) != 0:
                _split_count += len(selected)

            _return_data:List = []

            if (len(_new) == 0) or (len(_new) == 1 and _split_count == 0):
                _return_data = self._get_modules()
                return self._clean_options(_return_data, '' if len(_new) == 0 or len(_new[0]) == 0 else _new[0], "Modules")
            elif (len(_new) == 1 and _split_count == 1) or (len(_new) == 2 and _split_count == 1):
                _return_data = self._get_submodules(_new[0])
                return self._clean_options(_return_data, '' if len(_new) == 1 or len(_new[1]) == 0 else _new[1], "Submodules")
            elif (len(_new) == 2 and _split_count == 2) or (len(_new) == 3 and _split_count == 2):
                _return_data = self._get_packages(_new[0], _new[1])
                return self._clean_options(_return_data, '' if len(_new) == 2 or len(_new[2]) == 0 else _new[2], "Packages")

        except Exception as e:
            raise e
            