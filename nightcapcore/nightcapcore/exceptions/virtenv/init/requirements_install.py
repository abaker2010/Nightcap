from .base import PyenvInitException

class PyenvRequirementsInstallException(PyenvInitException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)