from nightcapcore import Command, Printer
from nightcapcore.package.information import PackageInformation
from nightcapcore.database.mongo.mongo_report import MongoReportDatabase
from nightcapcore.exceptions.reporting.reporting import ReportingExcutionException
from nightcapcore.package.report_view.report_view import ReportView
from nightcapcore.projects.projects import Project
from nightcapcore.reporting.report_data import ReportData
from datetime import datetime, timezone

class ReportingCommand(Command):
    def __init__(self, project: Project, package_information: PackageInformation, report_data: ReportData, report_design: ReportView) -> None:
        super().__init__()
        self.project = project
        self.package_information = package_information
        self.report_data = report_data
        self.report_design = report_design
        self.printer = Printer()
        self._db = MongoReportDatabase()

    def execute(self) -> dict:
        try:
            format = '%b %d %Y %I:%M%p'
            run_time = datetime.strftime(datetime.now(), format)
            # print(run_time)
            # print(type(run_time))
            self.printer.print_underlined_header(f"Reporting")
            self.printer.item_1(f"Project (ID) :: {self.project.id}")
            self.printer.item_1(f"Project (NAME) :: {self.project.name}")
            # self.printer.item_1(f"Report Data :: {self.report_data.to_json()}")
            self.printer.print_formatted_check("Reporting Done")
            _submitted = self._db.create_report({
                    "project" : self.project, "package_information" : self.package_information, 
                    "ran_at" : run_time,
                    "report_data" : self.report_data, "report_design" : self.report_design})
            if _submitted.acknowledged:
                self.printer.item_1(f"Inserted ID :: {_submitted.inserted_id}")
        except  ReportingExcutionException as ree:
            self.printer.print_error(f"ERROR EXECUTING REPORTING :: {ree}")
        