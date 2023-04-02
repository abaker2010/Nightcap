from typing import Dict

class Language(object):
    def __init__(self, language: str = None, version: str = None, 
                env_name: str = None, requirements_file: str = None, requirements: Dict[str, str] = None) -> None:
        self.language = language
        self.version = version
        self.env_name = env_name
        self.requirements_file = requirements_file if requirements_file != "None" else None
        self.requirements = requirements

    def to_json(self):
        return self.__dict__

