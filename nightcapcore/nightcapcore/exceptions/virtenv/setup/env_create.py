from .base import EnvSetupException

class VirtenvCreateException(EnvSetupException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)