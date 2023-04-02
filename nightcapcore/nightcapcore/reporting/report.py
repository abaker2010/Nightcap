from __future__ import annotations
from nightcapcore.package.information import PackageInformation
from nightcapcore.projects.projects import Project
from nightcapcore.reporting.report_data import ReportData
from nightcapcore.package.report_view.report_view import ReportView
from bson.objectid import ObjectId
from datetime import datetime, timezone

class Report(object):
    def __init__(self, data: dict = None) -> None: #project: Project, package_information: PackageInformation, report_data: ReportData, report_design: ReportView ) -> None:
        self.id = None if data == None or '_id' not in data.keys() else str(data["_id"])
        self.ran_at = None if data == None or 'ran_at' not in data.keys() else data['ran_at']

        if isinstance(data['project'], Project):
            self.project = data['project']
        else:
            self.project = Project.from_json(data['project'])

        if isinstance(data['package_information'], PackageInformation):
            self.package_information = data['package_information']
        else:
            self.package_information = PackageInformation.from_json(data['package_information'])
        

        if isinstance(data['report_data'], ReportData):
            self.report_data = data['report_data']
        else:
            self.report_data = ReportData(data['report_data'])

        
        if isinstance(data['report_design'], ReportView):
            self.report_design = data['report_design']
        else:
            self.report_design = ReportView.from_json(data['report_design'])

    def to_json(self):
        data:dict =  self.__dict__
        if data['id'] == None:
            del data['id']
        return data

    @staticmethod
    def from_json(data: dict) -> Report:
        return Report(data)

    def new_report(self):
        return {"project_id" : self.project_id, "report_data" : self.report_data.to_json()}