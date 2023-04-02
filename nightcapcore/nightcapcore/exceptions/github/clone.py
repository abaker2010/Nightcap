from .base import GithubException

class GithubCloneException(GithubException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)