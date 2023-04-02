
import os
import json
import configparser
from typing import List
from ast import literal_eval
from nightcapcore.projects.projects import Project
from nightcapcore.singleton.singleton import Singleton
from nightcapcore.lang_supported import LanguageSupported
from nightcapcore.container.docker_manager import DockerManager
from nightcapcore.database.mongo_manager import MongoManager

class NightcapCLIConfiguration(metaclass=Singleton):
    def __init__(self):
        # region Getting config information
        conf = configparser.RawConfigParser()
        _path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "nightcapcore.cfg"
        )
        conf.read(_path)
        self.config = conf
        # endregion

        # region 
        # ToDo: Make this config section in to a NightCAPManager
        self.verbosity = self.config.getboolean("NIGHTCAPCORE", "verbose")

        self.buildNumber = int(self.config.get("BUILD_DATA", "build"))
        self.versionNumber = int(self.config.get("BUILD_DATA", "version"))
        self.mainbranch = self.config.getboolean("BUILD_DATA", "main_branch")

        # self.languages_supported:List[LanguageSupported] = []

        self.project:Project = None

        # for k, v in dict(self.config.items("LANGS_SUPPORTED")).items():
        #     _lang_detials = literal_eval(v)
        #     _tmp = LanguageSupported(k, _lang_detials['version'], _lang_detials['enabled'])
        #     self.languages_supported.append(_tmp)

        # endregion

        self.isDaemon = self.config.getboolean("DOCKER", "isDaemon", fallback=False)
        self.docker_ip = self.config.get("DOCKER", "ip", fallback=None)
        self.docker_port = self.config.get("DOCKER", "port", fallback=None)

        # region 
        # ToDo: Make this config section in to a MongoManager
        # self.mongo_proc = self.config.get("MONGOSERVER", "proc")
        self.mongo_ip = self.config.get("MONGOSERVER", "ip")
        self.mongo_port = self.config.get("MONGOSERVER", "port")
        self.mongo_dbname = self.config.get("MONGOSERVER", "db_name")
        self.mongo_dbusername = self.config.get("MONGOSERVER", "username")
        self.mongo_dbpasswd = self.config.get("MONGOSERVER", "password")
        self.mongo_shutdown = self.config.getboolean("MONGOSERVER", "shutdown_on_exit") 
        
        self.mongoManager = MongoManager.connect(self.mongo_ip, self.mongo_port, self.mongo_dbusername, \
                                                    self.mongo_dbpasswd, 'nightcap')
        self.mongoAvailable = self.mongoManager.check_connection()


        # self.mongoManager.connect(self.mongo_ip, self.mongo_port, self.mongo_dbusername, self.mongo_dbpasswd)
        # endregion

        try:
            self.dockerManager:DockerManager = DockerManager()
            self.dockerManager.connect(self.isDaemon, self.docker_ip, self.docker_port)
            self.dockerManager.addContainersFromJson(json.loads(self.config.get("DOCKER", "containers", fallback=None)))   
            self.dockerAvailable = True    
        except Exception as e:
            self.dockerAvailable = False
            # print(type(e))
            # print("Failed to conncet to docker daemon")
        

    def save(self) -> None:
        _path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "nightcapcore.cfg"
        )
        with open(_path, "w") as configfile:
            self.config.write(configfile)
