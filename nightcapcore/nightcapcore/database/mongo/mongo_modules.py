
# region Imports
from typing import List
from nightcapcore.printers import Printer
from nightcapcore.package.module.module import Module
from nightcapcore.singleton.singleton import Singleton
from nightcapcore.database.mongo.connections.mongo_operation_connector import MongoDatabaseOperationsConnection
# endregion


class MongoModuleDatabase(MongoDatabaseOperationsConnection, metaclass=Singleton):
    """

    This class is used interact with the mongo databse

    ...

    Attributes
    ----------
        _db: -> MongoClient
            the connection to the db

    Methods
    -------
        Accessible
        -------
            create(self, module: str = None): -> None
                addes a new module to the database

            read(self): -> Any
                this will read the database

            update(self): -> pass
                for override when implemented

            delete(self): -> pass
                for override when implemented

            find(self, module: str = None): -> Any
                returns the results of the find query

            find_one(self, module: str = None): -> Any
                returns the results of the find one query

            check_module_path(self, path: list): -> Any
                returns the module if exists

            get_all_modules(self): -> Any
                returns all of the modules

            module_install(self, module: str): -> None
                tries to install the module


            module_try_unintall(self, module: str): -> None
                tries to uninstall the module
    """

    # region Init
    def __init__(self):
        MongoDatabaseOperationsConnection.__init__(self)
        self._db = self.client[self.conf.config["MONGOSERVER"]["db_name"]]["modules"]
        self.printer = Printer()

    # endregion

    # region Create
    def create(self, module: str = None):
        self._db.insert_one({"type": module})

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
    def find(self, module: str = None):
        return self._db.find({"type": module})

    # endregion

    # region Find One
    def find_one(self, module: str = None):
        return self._db.find_one({"type": module})

    # endregion

    # region Check Module Path
    def check_module_path(self, path: list):
        return self.find(path[0])

    # endregion

    # region Get All Modules
    def get_all_modules(self) -> List[Module]:
        _modules:List[Module] = []
        _doc = self.read()
        for m in list(_doc):
            _modules.append(Module(**m))

        return _modules
    # endregion

    # region Install Module
    def module_install(self, module: str):
        _moduleexists = self.find(module)
        if _moduleexists.count() == 0:
            self.create(module)

    # endregion

    # region Uninstall Module
    def module_try_unintall(self, module: str):
        _moduleexists = self.find_one(module)
        self._db.remove(_moduleexists)
        self.printer.print_formatted_additional(
            text="Deleted module entry", leadingTab=3
        )

    # endregion
