from .base import Validate
from typing import List, Literal, Tuple
from nightcapcore.exceptions.publisher import PublisherValidationException
from nightcapcore.database.mongo.mongo_modules import MongoModuleDatabase
from nightcapcore.database.mongo.mongo_packages import MongoPackagesDatabase
from nightcapcore.database.mongo.mongo_submodules import MongoSubModuleDatabase

class CMDValidate(Validate):

    def __init__(self, current_opts: List[str]) -> None:
        super().__init__()
        self.current_opts = current_opts
        self.modules_db = MongoModuleDatabase()
        self.submodules_db = MongoSubModuleDatabase()
        self.packages_db = MongoPackagesDatabase()

    # region validate user wanted path
    def validate(self, data: List[str]) -> Tuple[bool, List]:
        try:
            _tmp_path = []
            
            for opt in self.current_opts:
                _tmp_path.append(opt)

            if len(self.current_opts) == 0:
                if len(data) == 1:
                    _tmp_path = data
                elif len(data) == 2:
                    _tmp_path = data
                elif len(data) == 3:
                    _tmp_path = data
                else:
                    raise PublisherValidationException("ERROR WITH PUBLISHER :: INVLID PATH")

            elif len(self.current_opts) == 1:

                if len(data) == 1:
                    _tmp_path.append(data[0])
                elif len(data) == 2:
                    _tmp_path.append(data[0])
                    _tmp_path.append(data[1])
                elif len(data) == 3:
                    _tmp_path = data
                else:
                    raise PublisherValidationException("ERROR WITH PUBLISHER :: INVLID PATH")
            elif len(self.current_opts) == 2:

                if len(data) == 1:
                    _tmp_path.append(data[0])
                elif len(data) == 2:
                    _tmp_path.append(data[0])
                    _tmp_path.append(data[1])
                elif len(data) == 3:
                    _tmp_path = data
                else:
                    raise PublisherValidationException("ERROR WITH PUBLISHER :: INVLID PATH")
            else:
                pass

            if self._check_current_path(_tmp_path):

                return (True, _tmp_path)
            else:
                raise PublisherValidationException(f"ERROR WITH VALIDATION :: INVLID PATH :: {_tmp_path}")


        except Exception as e:
            raise Exception(f"VALIDATION ERROR :: {e}")
    # endregion

    # region Get popped object
    def _get_pop(self, list: list) -> Literal:
        _pop = 0

        if self.current_opts == []:
            return 0
        else:
            if len(self.current_opts) == 1:
                return 1
            elif len(self.current_opts) == 2:
                if self.current_opts[0] != list[0]:
                    _pop = 2
                elif self.current_opts[1] != list[1]:
                    _pop = 1
                return _pop
            elif len(self.current_opts) == 3:
                return 3
    # endregion

    # region Check module tpye
    def _check_module_types(self, path: list) -> bool:
        return False if self.modules_db.check_module_path(path).count() == 0 else True
    # endregion
    
    # region Check submodule
    def _check_sub_module(self, path: list) -> bool:
        return (
            False
            if self.submodules_db.check_submodule_path(path).count() == 0
            else True
        )
    # endregion

    # region Check package
    def _check_packages(self, selected) -> bool:
        return self.packages_db.check_package_path(selected)
    # endregion

    # region Check current path
    def _check_current_path(self, path: list) -> bool:
        if len(path) == 1:
            return self._check_module_types(path)
        elif len(path) == 2:
            return self._check_module_types(path) & self._check_sub_module(path)
        elif len(path) == 3:
            return (
                self._check_module_types(path)
                & self._check_sub_module(path)
                & self._check_packages(path)
            )
        return False
    # endregion