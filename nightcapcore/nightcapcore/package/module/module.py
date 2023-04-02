from bson import ObjectId

class Module(object):
    def __init__(self, _id: ObjectId, type: str) -> None:
        self._id = _id
        self.type = type

    def to_json(self):
        return self.__dict__