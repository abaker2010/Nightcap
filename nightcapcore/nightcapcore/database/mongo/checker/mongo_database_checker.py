
# region Import
from nightcapcore.singleton.singleton import Singleton
from ..connections import MongoDatabaseConnection

# endregion


class MongoDatabaseChecker(MongoDatabaseConnection, metaclass=Singleton):
    """

    This class is used to check the Docker Continers

    ...

    Methods
    -------
        Accessible
        -------
            check_database(self): -> bool
                returns a boolean depending on if the docker container is running

            initialize_database(self): -> None
                initializes the databases

    """

    # region Init
    def __init__(self):
        super().__init__()

    # endregion

    # region Check Database
    def check_database(self):
        if self.db_name in self.client.list_database_names():
            return True
        else:
            return False

    # endregion

    # region Init Database
    def initialize_database(self):
        mydict = {"name": "John", "address": "Highway 37"}
        self.client[self.db_name]["holder"].insert_one(mydict)

    # endregion

    def test(self):
        print("Called testing")