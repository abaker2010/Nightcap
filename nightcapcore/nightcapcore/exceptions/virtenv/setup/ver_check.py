from .base import EnvSetupException

class VirtenvVersionCheckException(EnvSetupException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)