from __future__ import annotations
from nightcapcore.database.mongo.interfaces import MongoDatabaseInterface

class MongoManager(MongoDatabaseInterface):
    def __init__(self, ip:str, port:str, uname:str, passwd:str, db_name: str) -> None:
        super().__init__(ip=ip, port=port, username=uname, password=passwd)
        try:
            self.available = True

        except Exception as e:
            self.available = False
            raise Exception("Unable to connect to MongoDB Instance")
    
    def check_connection(self) -> bool:
        try:
            self.client.server_info()
            return True
        except Exception as e:
            return False

    

    @staticmethod
    def connect(ip:str, port:str, uname:str, passwd:str, db_name: str) -> MongoManager:
        return MongoManager(ip, port, uname, passwd, db_name)
        
