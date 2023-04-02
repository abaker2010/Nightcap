from .author import Author
from .information import PackageInformation
from .meta import MetaData
from .report_view import ReportView

class Package(object):
    def __init__(self, data: dict = None) -> None:
        self.author = Author(**data['author']) if data != None else Author()
        self.package_information = PackageInformation(**data['package_information']) if data != None else PackageInformation()
        self.package_for = MetaData(**data['package_for']) if data != None else MetaData()
        self.report_design = None if data == None or "report_design" not in data.keys() else ReportView(**data['report_design'])
        self.id = None if data == None or '_id' not in data.keys() else str(data["_id"])
    
    def to_json(self):
        return self.__dict__