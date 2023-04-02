
# region Imports
from typing import List
from nightcapcore.printers.print import Printer
from nightcapcore.singleton.singleton import Singleton
from nightcapcore.package.submodule.submodule import Submodule
from nightcapcore.database.mongo.mongo_packages import MongoPackagesDatabase
from nightcapcore.database.mongo.connections.mongo_operation_connector import MongoDatabaseOperationsConnection
# endregion


class MongoSubModuleDatabase(MongoDatabaseOperationsConnection, metaclass=Singleton):
    """

    This class is used to help validate user input to the console

    ...

    Attributes
    ----------
        _db: -> MongoClient

    Methods
    -------
        Accessible
        -------
            create(self, module: str = None, submodule: str = None): -> None
                tries to insert a submodule into the db

            read(self): -> Any
                returns all items in the db

            update(self): -> pass
                Child will implement

            delete(self) -> pass
                Child will implement

            find(self, module: str = None, submodule: str = None): -> dict
                returns a dict if the submodules are found

            find_one(self, module: str = None, submodule: str = None): -> dict
                returns a dict if the submodule is found

            find_submodules(self, module: str = None): -> dict
                find all submodules of a module type

            check_submodule_path(self, path: list): -> dict
                checks the submodules path

            submodule_install(self, module: str, submodule: str): -> None
                tries to install the submodule

            submodule_try_uninstall(self, module: str, submodule: str): -> None
                tries to uninstall the submodule
    """

    # region Init
    def __init__(self):
        MongoDatabaseOperationsConnection.__init__(self)
        self._db = self.client[self.conf.config["MONGOSERVER"]["db_name"]]["submodules"]
        self.printer = Printer()

    # endregion

    # region Create
    def create(self, module: str = None, submodule: str = None):
        self._db.insert_one({"module": module, "type": submodule})
        # self.printer.print_formatted_check(text="Added to submodules db")

    # endregion

    # region Read
    def read(self):
        return self._db.find()

    # endregion

    # region Update
    def update(self):
        pass

    # endregion

    # region Delete
    def delete(self):
        pass

    # endregion

    def drop(self):
        self._db.drop()

    # region Find
    def find(self, module: str = None, submodule: str = None):
        return self._db.find(
            {"$and": [{"module": {"$eq": module}}, {"type": {"$eq": submodule}}]}
        )

    # endregion

    # region Find One
    def find_one(self, module: str = None, submodule: str = None):
        return self._db.find_one({"module": module, "type": submodule})

    # endregion

    # region Find Submodules
    def find_submodules(self, module: str = None) -> List[Submodule]:
        _submodules:List[Submodule] = []
        _subs = self._db.find({"module": module})
        for sub in _subs:
            _submodules.append(Submodule(**sub))
    
        return _submodules

    # endregion

    # region Check submodule path
    def check_submodule_path(self, path: list):
        # return self.find_one(path[0], path[1])
        _subpath = self._db.find(
            {"$and": [{"module": {"$eq": path[0]}}, {"type": {"$eq": path[1]}}]}
        )
        return _subpath

    # endregion

    # region Install Submodule
    def submodule_install(self, module: str, submodule: str):
        _submoduleexists = self.find(module, submodule)
        if _submoduleexists.count() == 0:
            self.create(module, submodule)
        else:
            pass

    # endregion

    # region Uninstall Submodule
    def submodule_try_uninstall(self, module: str, submodule: str):
        _count = MongoPackagesDatabase().find_packages(module, submodule).count()
        if _count == 0:
            self.printer.debug(
                "Trying remove submodule:",
                self.find_one(module, submodule),
                # currentMode=self.conf.verbosity,
            )
            self._db.remove(self.find_one(module, submodule))
            self.printer.debug(
                "Deleted submodule entry", #currentMode=self.conf.verbosity
            )

    # endregion
