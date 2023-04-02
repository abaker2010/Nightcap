from bson import ObjectId

class Submodule(object):
    def __init__(self, _id: ObjectId, module: str, type: str) -> None:
        self._id = _id
        self.module = module
        self.type = type