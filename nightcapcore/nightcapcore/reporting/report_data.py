
class ReportData(object):
    def __init__(self, report_data: dict = None) -> None:
        self.data = report_data

    def to_json(self):
        return self.__dict__