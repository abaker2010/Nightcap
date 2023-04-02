from typing import List

class Filter(object):
    def __init__(self, cid: str = None, sid: str = None, 
                 name: str = None, replace: str = None,
                 replace_with: str = None, replace_on_save: str = None,
                 replace_on_save_with: str = None, regex: List[str] = None) -> None:
        self.cid = cid
        self.name = name
        self.replace = replace
        self.replace_with = replace_with
        self.replace_on_save = replace_on_save
        self.replace_on_save_with = replace_on_save_with
        self.regex = regex
        self.sid = sid

    def to_json(self):
        return self.__dict__