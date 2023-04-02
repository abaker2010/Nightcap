from .base import PublisherException

class PublisherValidationException(PublisherException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)