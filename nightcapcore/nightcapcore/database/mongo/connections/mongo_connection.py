
# region Import
from pymongo.errors import ServerSelectionTimeoutError
from nightcapcore import NightcapCLIConfiguration
from nightcapcore.database.mongo.interfaces.mongo_db_interface import MongoDatabaseInterface
# endregion


class MongoDatabaseConnection(MongoDatabaseInterface):
    """

    This class is used as an interface to connect to the Mongo Docker Container

    ...

    Attributes
    ----------
        ** Not including the MongoDatabaseInterface options

        conf: -> NightcapCLIConfiguration
        ip: -> str
        port: -> str
        name: -> str

        _db_name: -> str
        _uname: -> str
        _pass: -> str
    """

    def __init__(self):
        self.conf = NightcapCLIConfiguration()
        ip = self.conf.config["MONGOSERVER"]["ip"]
        port = self.conf.config["MONGOSERVER"]["port"]
        _db_name = self.conf.config["MONGOSERVER"]["db_name"]
        _uname = self.conf.config["MONGOSERVER"]["username"]
        _pass = self.conf.config["MONGOSERVER"]["password"]

        self.name = None
        if ip == None:
            raise Exception("Mongo Server IP not set")
        if port == None:
            raise Exception("Mongo Server Port not set")
        if _db_name == None:
            raise Exception("Mongo Server DB_Name not set")
        else:
            self.db_name = _db_name
        try:
            super().__init__(ip, port, _uname, _pass)
        except ServerSelectionTimeoutError as e:
            self.printer.print_error("FOUND CONNECTION ERROR MAYBE")
            raise e
