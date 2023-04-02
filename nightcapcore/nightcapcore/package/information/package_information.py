from __future__ import annotations
from ..params import EntryParam
from typing import Dict, List
from nightcapcore.package.github.github import Github
from nightcapcore.package.filters.base.filter import Filter
from nightcapcore.package.language.language import Language
from nightcapcore.package.filters.return_filters import ReturnFilters

class PackageInformation(object):

    def __init__(self, package_name: str = None, package_type: str = None, version: str = None, date: str = None,
                    imports: list = None, details: str = None, entry_file: str = None,
                    entry_file_optional_params: dict = None, return_filters: dict = None, uid: str = None, language: dict = None,
                    github: dict = None, entry_class_name: str = None) -> None:
        self.package_name:str = package_name
        self.package_type:str = package_type
        self.version:str = version
        self.date:str = date
        self.imports:List = imports 
        self.details:str = details
        self.entry_file:str = entry_file 
        self.language:Language = Language(**language) if language != None else Language()
        self.github:Github = Github() if github == None else Github(**github) 
        self.entry_file_optional_params:Dict[str, EntryParam] = None if \
                                                            entry_file_optional_params == {} or entry_file_optional_params == None else \
                                                            {key: EntryParam(**value) for (key, value) in entry_file_optional_params.items()}
        self.entry_class_name:str = entry_class_name

        self.return_filters:ReturnFilters = None if \
                                                    return_filters == {} or return_filters == None else \
                                                            ReturnFilters({key: Filter(**value) for (key, value) in return_filters.items()})
        # self.uid:str = uid

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(data: dict) -> PackageInformation:
        return PackageInformation(**data)
        