from pymongo.cursor import Cursor
from bson.objectid import ObjectId
from nightcapcore.singleton.singleton import Singleton
from nightcapcore.database.mongo.connections.mongo_operation_connector import MongoDatabaseOperationsConnection

class MongoTasksDatabase(MongoDatabaseOperationsConnection, metaclass=Singleton):
    def __init__(self):
        MongoDatabaseOperationsConnection.__init__(self)
        self._db = self.client[self.conf.config["MONGOSERVER"]["db_name"]]["tasks"]

    #region Create
    def create(self, task: dict) -> None:
        self._db.insert_one(task)
    #endregion

    # region Read
    def read(self) -> Cursor:
        return self._db.find()

    # endregion

    # region Delete
    def delete(self, puid: ObjectId) -> None:
        self._db.delete_one({"_id": puid})
    # endregion
    