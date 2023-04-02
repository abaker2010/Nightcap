
# region Import
import json
from typing import List
from pymongo.cursor import Cursor
from bson.objectid import ObjectId
from nightcapcore.reporting.report import Report
from nightcapcore.projects.projects import Project
from nightcapcore.singleton.singleton import Singleton
from pymongo.collection import InsertOneResult, DeleteResult
from nightcapcore.helpers.json.encoder import NightcapJSONEncoder
from nightcapcore.database.mongo.connections.mongo_operation_connector import MongoDatabaseOperationsConnection
# endregion

class MongoReportDatabase(MongoDatabaseOperationsConnection, metaclass=Singleton):
    def __init__(self):
        MongoDatabaseOperationsConnection.__init__(self)
        self._db = self.client[self.conf.config["MONGOSERVER"]["db_name"]]["report"]

    # region Create
    def create(self, report: Report) -> InsertOneResult:
        # return self._db.insert_one(report.new_report())
        return self._db.insert_one(json.loads(json.dumps(report, cls=NightcapJSONEncoder)))
        
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
        return self._db.delete_one({"_id": puid})

    # endregion

    def drop(self) -> None:
        self._db.drop()


    def get_reports(self, project: Project) -> List[Report]:
        _reports:List[Report] = []

        _data = self._db.find(
            {
                "$and": [
                        {  
                            "project.id" : 
                            {
                                "$eq" : str(project.id)
                            }
                        },
                ]
            }
        )
        for rep in _data:
            _reports.append(Report.from_json(rep))

        return _reports


    def get_single_report(self, projectID: str, reportID: str) -> Report:
        _data = self._db.find_one(
            {
                "$and": [
                        {  
                            "_id" : 
                            {
                                "$eq" : ObjectId(reportID)
                            }
                        },
                        {  
                            "project.id" : 
                            {
                                "$eq" : str(projectID)
                            }
                        },
                ]
            }
        )
    
        if _data == None:
            return None
        else:
            return Report.from_json(_data)


    def create_report(self, data: dict) -> InsertOneResult:#project: Project, package_information: PackageInformation, report_data: ReportData, report_design: ReportView) -> InsertOneResult:
        _report = Report(data)#project, package_information, report_data, report_design)
        return self.create(_report)


    def list_reports(self) -> List[Report]:
        _reports:List[Report] = []

        for elem in self.read():
            _reports.append(Report.from_json(elem))
        
        return _reports


        