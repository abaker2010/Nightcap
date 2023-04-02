
class MetaData(object):
    def __init__(self, module: str = None, submodule: str = None) -> None:
        self.module = module
        self.submodule = submodule

    def to_json(self):
        return self.__dict__