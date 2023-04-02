
# region Import
import json
from typing import List
from pymongo.cursor import Cursor
from bson.objectid import ObjectId
# from nightcapcore.reporting.report import Report
from nightcapcore.projects.projects import Project
from nightcapcore.singleton.singleton import Singleton
from pymongo.collection import InsertOneResult, DeleteResult
from nightcapcore.helpers.json.encoder import NightcapJSONEncoder
from nightcapcore.database.mongo.connections.mongo_operation_connector import MongoDatabaseOperationsConnection
# endregion

class MongoLanguagesDatabase(MongoDatabaseOperationsConnection, metaclass=Singleton):
    def __init__(self):
        MongoDatabaseOperationsConnection.__init__(self)
        self._db = self.client[self.conf.config["MONGOSERVER"]["db_name"]]["language_support"]

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
        return self._db.delete_one({"_id": puid})

    # endregion

    def drop(self) -> None:
        self._db.drop()


    def get_language_details(self, language: str) -> List:
        _reports:List = []

        # _data = self._db.find(
        #     {
        #         "$and": [
        #                 {  
        #                     "project.id" : 
        #                     {
        #                         "$eq" : str(project.id)
        #                     }
        #                 },
        #         ]
        #     }
        # )
        # for rep in _data:
        #     _reports.append(Report.from_json(rep))

        return _reports

    def get_supported_languages(self) -> List:
        _reports:List = []

        _data = self.read()
        # .find(
        #     {
        #         "$and": [
        #                 {  
        #                     "project.id" : 
        #                     {
        #                         "$eq" : str(project.id)
        #                     }
        #                 },
        #         ]
        #     }
        # )

        return _data