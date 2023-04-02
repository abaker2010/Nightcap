from nightcapcore.lang_supported.enum.lang_enum import LangEnum

class Github(object):
    def __init__(self, url: str = None, commit_id: str = None) -> None:
                
        self.url = url
        self.commit_id = commit_id
        # self.lang:LangEnum = LangEnum.from_string(language) if language != None else None
        # self.version = version
        # self.requirements = requirements

    def to_json(self):
        return self.__dict__

