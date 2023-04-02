class EntryParam(object):
    def __init__(self, name: str, value: str, description: str, corresponding_flag: str = None,
                param_needed: str = "False", required: str = "False", default: str = "None") -> None:
        self.name = name
        self.value = value
        self.corresponding_flag = corresponding_flag
        self.description = description
        self.param_needed = (True if param_needed.lower() == 'true' else False) if type(param_needed) == str else param_needed
        self.required =  (True if required.lower() == 'true' else False) if type(required) == str else required
        self.default = default
    
    def to_json(self):
        return self.__dict__