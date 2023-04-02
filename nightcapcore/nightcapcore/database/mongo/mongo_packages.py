
# region Import
import os
import json
from typing import Any, List
from pymongo.cursor import Cursor
from pymongo.results import DeleteResult
from bson.objectid import ObjectId
from colorama.ansi import Fore, Style
from nightcapcore.printers import Printer
from nightcapcore.package.package import Package
from nightcapcore.singleton.singleton import Singleton
from nightcapcore.helpers.json.encoder import NightcapJSONEncoder
from nightcapcore.exceptions.database.already_installed import DatabaseAlreadyInstallException
from nightcapcore.database.mongo.connections.mongo_operation_connector import MongoDatabaseOperationsConnection
from nightcappackages.classes.paths.pathsenum import NightcapPackagesPathsEnum
from nightcappackages.classes.paths.paths import NightcapPackagesPaths
# endregion

class MongoPackagesDatabase(MongoDatabaseOperationsConnection, metaclass=Singleton):
    """

    This class is used to interact with the packages database

    ...

    Attributes
    ----------
        _db: -> MongoClient
            MongoClient

    Methods
    -------
        Accessible
        -------
            create(self, pkg: dict): -> None
                Allows the users to insert an entry

            read(self): -> Any
                reads the db

            delete(self, puid: ObjectId): -> None
                delete an entry

            get_class_run_path(self, pkg_config: dict = None): -> str
                get the package run path for the system

            check_package_path(self, path: list): -> bool
                check if the package exists

            package_params(self, selected: list): -> None
                prints out the package params

            get_package_config(self, parentmodules: list): -> dict
                gets the package configuration

            packages(self, parentmodules: list, isDetailed: bool = False): -> Any
                returns a list of packages if any

            find_package(self, package: dict = None): -> dict
                trys to find a package

            find_packages(self, module: str = None, submodule: str = None): -> dict
                tries to find many packages

            install(self, package: dict = None): -> bool
                will try to install a new package

            get_all_packages(self): -> dict
                returns all of the packages installed
    """

    # region Init
    def __init__(self) -> None:
        MongoDatabaseOperationsConnection.__init__(self)
        self._db = self.client[self.conf.config["MONGOSERVER"]["db_name"]]["packages"]
        self.printer = Printer()

    # endregion

    # region Create
    def create(self, pkg: dict) -> None:
        self._db.insert_one(pkg)

    # endregion

    # region Read
    def read(self) -> Cursor:
        return self._db.find()

    # endregion

    # region Update
    def update(self) -> None:
        pass

    # endregion

    # region Delete
    def delete(self, puid: ObjectId) -> None:
        result:DeleteResult = self._db.delete_one({"_id": puid})
        # print("Delete count : ", result.deleted_count)
    # endregion

    def drop(self) -> None:
        self._db.drop()

    # region Uninstall Package
    def prackage_try_uninstall(self, pkg: Package):
        self._db.delete_one({"_id" : ObjectId(pkg.id)})
    # endregion

    # region Find Package
    def find_package_by_id(self, pkg_id: str) -> Any:
        return self._db.find_one({"_id" : ObjectId(pkg_id)})
    # endregion

    # region Get local package run path
    def get_package_run_path(self, pkg: Package = None):
        try:
            _file = (
                os.sep.join(pkg.package_information.entry_file)
                if isinstance(pkg.package_information.entry_file, list)
                else pkg.package_information.entry_file
            )

            if pkg.package_information.entry_class_name != None:
                _file = _file.replace(".py", "")

            _import = [pkg.package_for.module, pkg.package_for.submodule,
                        pkg.package_information.package_name, _file]

            if pkg.package_information.entry_class_name != None:
                _import.append(pkg.package_information.entry_class_name)

            if pkg.package_information.entry_class_name != None:
                _path = NightcapPackagesPaths().generate_import_path(
                    NightcapPackagesPathsEnum.PackagesBase,
                    _import
                )
            else:
                _path = NightcapPackagesPaths().generate_path(
                    NightcapPackagesPathsEnum.PackagesBase,
                    _import
                )
                
            return _path
        except Exception as e:
            raise Exception("ERROR FINDING RUN PATH :: %s" % e)

    # endregion

    # region Check package path
    def check_package_path(self, path: list) -> bool:
        _module = path[0]
        _submodule = path[1]
        _package = path[2]
        _ = self._db.find_one(
            {
                "$and": [
                    {
                        "package_for.module": {"$eq": _module},
                        "package_for.submodule": {"$eq": _submodule},
                        "package_information.package_name": {"$eq": _package},
                    }
                ]
            }
        )
        return False if _ == None else True
    # endregion

    # region Add Default Package Params
    def set_default_package_params(self, pkg: Package = None):
        self.printer.debug("Trying to set default params")
        try:
            _tmp = {}
            for k,v in pkg.package_information.entry_file_optional_params.items():
                _tmp[k] = v.__dict__

            result = self._db.update_one({"_id" : ObjectId(pkg.id)}, {"$set": {"package_information.entry_file_optional_params" : _tmp}})
            self.printer.debug(str(result.matched_count) + " : " + str(result.modified_count)) #, currentMode=NightcapCLIConfiguration().verbosity)
            return True
        except Exception as e:
            self.printer.print_error(e)
            return False
    # endregion

    # region Get package config
    def get_package_config(self, parentmodules: list) -> Any:
        return self._db.find_one(
            {
                "$and": [
                    {
                        "package_for.module": {"$eq": parentmodules[0]},
                        "package_for.submodule": {"$eq": parentmodules[1]},
                        "package_information.package_name": {"$eq": parentmodules[2]},
                    }
                ]
            }
        )
    # endregion

    # region Get Options Packages
    def packages(self, parentmodules: list, isDetailed: bool = False) -> list:
        _module = parentmodules[0]
        _submodule = parentmodules[1]
        _npackages = self._db.find(
            {
                "$and": [
                    {
                        "package_for.module": {"$eq": _module},
                        "package_for.submodule": {"$eq": _submodule},
                    }
                ]
            }
        )

        npackages = []
        for _npkg in _npackages:
            npackages.append(_npkg)

        if isDetailed:
            _packages = list(map(lambda v: v, npackages))
            packages = []
            h = """%s (%s) %s|%s %s %s| %s""" % (
                (Fore.GREEN + "Package Name" + Fore.CYAN),
                ("Version"),
                (Fore.BLUE),
                (Fore.CYAN),
                ("Developer"),
                (Fore.BLUE),
                (Fore.YELLOW + "Details" + Style.RESET_ALL),
            )
            h1 = Fore.CYAN + "-" * len(h) + Style.RESET_ALL
            packages.append("\n")
            packages.append(h)
            packages.append(h1)
            for pkt in _packages:
                h1 = pkt["package_information"]["package_name"]
                h2 = pkt["package_information"]["details"]
                h3 = pkt["package_information"]["version"]
                h4 = pkt["author"]["creator"]
                p = """\t%s (%s) %s|%s %s %s| %s""" % (
                    (Fore.GREEN + h1 + Fore.CYAN),
                    (h3),
                    (Fore.BLUE),
                    (Fore.CYAN),
                    (h4),
                    (Fore.BLUE),
                    (Fore.YELLOW + h2 + Style.RESET_ALL),
                )
                packages.append(p)
        else:
            packages = list(
                map(lambda v: v["package_information"]["package_name"], list(npackages))
            )
        return packages

    # endregion

    # region Find Package
    def find_package(self, package: dict = None) -> Any:
        return self._db.find_one(package)
    # endregion

    # region Find Packages With Full Path
    def find_package_with_name(self, module: str = None, submodule: str = None, name: str = None):
        return self._db.find(
            {
                "$and": [
                    {
                        "package_for.module": {"$eq": module},
                        "package_for.submodule": {"$eq": submodule},
                        "package_information.package_name": {"$eq": name}
                    }
                ]
            }
        )
    # endregion

    # region Find Packages
    def find_packages(self, module: str = None, submodule: str = None) -> Cursor:
        return self._db.find(
            {
                "$and": [
                    {
                        "package_for.module": {"$eq": module},
                        "package_for.submodule": {"$eq": submodule},
                    }
                ]
            }
        )
    # endregion

    #region Get Packages List
    def get_packages_list(self, module: str = None, submodule: str = None) -> List[Package]:
        _list:List[Package] = []
        _packages = self._db.find(
                                {
                                    "$and": [
                                        {
                                            "package_for.module": {"$eq": module},
                                            "package_for.submodule": {"$eq": submodule},
                                        }
                                    ]
                                }
                            )
        for p in _packages:
            try:
                _list.append(Package(p))
            except Exception as e:
                print(str(e))

        return _list
    #endregion

    # region Install
    def installable(self, package: Package = None) -> bool:
        _pkg = json.loads(json.dumps(package, cls=NightcapJSONEncoder))
        _packages_like = self.find_package_with_name(package.package_for.module, package.package_for.submodule, package.package_information.package_name)

        if self.find_package(_pkg) == None and _packages_like.count() == 0:
            try:
                self.create(_pkg)
                return True
            except Exception as e:
                self.printer.print_error(e)
                return False
        else:
            raise DatabaseAlreadyInstallException("ERROR INSTALLING :: PACKAGE ALREADY INSTALLED")

    # endregion

    # region get all packages
    def get_all_packages(self) -> Cursor:
        return self.read()
    # endregion


    # region get all github packages
    def get_all_github(self) -> Cursor:
        return self._db.find(
            {
               "package_information.github" : {"$exists" : True}
            }
        )

    # endregion