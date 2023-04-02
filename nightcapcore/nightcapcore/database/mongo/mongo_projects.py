
# region Import
from typing import List
from pymongo.cursor import Cursor
from bson.objectid import ObjectId
from nightcapcore.printers.print import Printer
from pymongo.collection import InsertOneResult, DeleteResult
from nightcapcore.projects.projects import Project
from nightcapcore.singleton.singleton import Singleton
from nightcapcore.database.mongo.connections.mongo_operation_connector import MongoDatabaseOperationsConnection
from nightcapcore.exceptions.database.already_exists import DatabaseAlreadyExistsException
# endregion

class MongoProjectsDatabase(MongoDatabaseOperationsConnection, metaclass=Singleton):
    def __init__(self):
        MongoDatabaseOperationsConnection.__init__(self)
        self._db = self.client[self.conf.config["MONGOSERVER"]["db_name"]]["projects"]
        self.printer = Printer()
    
    # region Create
    def create(self, project: Project) -> InsertOneResult:
        return self._db.insert_one(project.new_project())
        
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
    def delete(self, puid: ObjectId) -> DeleteResult:
        result:DeleteResult =  self._db.delete_one({"_id": ObjectId(puid)})
        return result
    # endregion

    def drop(self) -> None:
        self._db.drop()


    def _exists(self, project: Project) -> bool:
        return False if  self._db.find(
            {
                "name" : {"$eq" : project.name}
            }
        ).count() == 0 else True

    def _get_project_id(self, project: Project) -> Project:
        _proj = self._db.find_one({
            "name" : {"$eq" : project.name}
        })

        return Project(_proj)

    def select_project(self, project_name: str):
        _tmp = Project({'name' : project_name})
        if self._exists(_tmp):
            return self._get_project_id(_tmp)
        else:
            raise Exception("PROJECT DOES NOT EXISTS")

    
    def create_project(self, project: Project) -> str:
        self.printer.print_underlined_header("Creating Project")
        self.printer.print_formatted_additional("Name", project.name)
        # print(self._exists(project).count())
        if (self._exists(project)):
            raise DatabaseAlreadyExistsException(f"PROJECT ({project.name}) :: ALREADY EXISTS")
        else:
            _isCreated = self.create(project)
            self.printer.item_1(_isCreated.inserted_id)
            return _isCreated.inserted_id

    def list_projects(self) -> List[Project]:
        _projects = []
        for p in self.read():
            _projects.append(Project(p))
        return _projects

    def delete_project(self, project: Project, override: bool = False) -> DeleteResult:
        try:
            if self._exists(project):
                _proj = self._get_project_id(project)
                if override == False:
                    if self.printer.input(f"Are you sure you want to delete ({_proj.name})? (Y/n)", defaultReturn=True):
                        _result = self.delete(ObjectId(_proj.id))
                        if _result.deleted_count == 1:
                            self.printer.print_formatted_check(f"Deleted ({_proj.name}) Successfully", endingBreaks=1)
                            return _result
                        else:
                            raise Exception(f"ERROR DELETING ({_proj.id} :: {_proj.name}) :: {_result.raw_result} :: {_result.deleted_count}")
                else:
                    _result = self.delete(ObjectId(_proj.id))
                    if _result.deleted_count == 1:
                        self.printer.print_formatted_check(f"Deleted ({_proj.name}) Successfully", endingBreaks=1)
                        return _result
                    else:
                        raise Exception(f"ERROR DELETING ({_proj.id} :: {_proj.name}) :: {_result.raw_result} :: {_result.deleted_count}")
            else:
                raise Exception("PROJECT DOES NOT EXIST")
        except Exception as e:
            raise Exception(e)

        