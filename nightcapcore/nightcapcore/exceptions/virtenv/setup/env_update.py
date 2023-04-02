from .base import EnvSetupException

class VirtenvUpdateException(EnvSetupException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)