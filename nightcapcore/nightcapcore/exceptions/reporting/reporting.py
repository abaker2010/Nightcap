from .base import ReportingException

class ReportingExcutionException(ReportingException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
