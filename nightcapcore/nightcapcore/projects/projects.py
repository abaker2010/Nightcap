from __future__ import annotations

class Project(object):
    def __init__(self, data: dict = None) -> None:
        if 'id' in data.keys():
            self.id = str(data['id'])
        else:
            self.id = None if data == None or '_id' not in data.keys() else str(data["_id"])
        self.name = None if data == None or 'name' not in data.keys() else data['name']

    def to_json(self):
        data:dict =  self.__dict__
        if data['id'] == None:
            del data['id']
        return data

    @staticmethod
    def from_json(data: dict) -> Project:
        return Project(data)

    def new_project(self):
        return {"name" : self.name}

