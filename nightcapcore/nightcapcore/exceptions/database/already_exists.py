from .base import DatabaseException

class DatabaseAlreadyExistsException(DatabaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)