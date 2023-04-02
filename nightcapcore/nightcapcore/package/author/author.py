
class Author(object):
    def __init__(self, first_name: str = None, last_name: str = None, github_url: str = None, personal_site: str = None) -> None:
        # self.creator = creator
        self.first_name = first_name
        self.last_name = last_name
        self.github_url = github_url
        self.personal_site = personal_site
        # self.creator = f"{self.first_name} {self.last_name}"

    def to_json(self):
        return self.__dict__

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} :: Github ({self.github_url}) :: Personal Site ({self.personal_site})"
