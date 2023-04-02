from .base import EnvSetupException

class VirtenvVersionInstallException(EnvSetupException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)