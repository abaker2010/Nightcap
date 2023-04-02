from typing import List, Dict
from docker.client import DockerClient, from_env
from nightcapcore.docker.docker_status import NightcapDockerStatus
from nightcapcore.singleton.singleton import Singleton
from nightcapcore.container.docker.docker_container import DockerContainer

class DockerManager(metaclass=Singleton):
    def __init__(self) -> None:
        super().__init__()
        self.containers:List[DockerContainer] = []
        self.client = None

    def connect(self, isDaemon: bool, domain: str = None, port: str = None):
        if isDaemon == True:
            if domain == None or port == None:
                raise Exception("USING REMOTE DOCKER DAEMON :: MUST HAVE IP/PORT IN CONFIG FILE")
            try:
                self.client = DockerClient("tcp://{}:{}".format(domain, port), timeout=2)
            except Exception as e:
                raise Exception("ERROR CONNECTING TO REMOTE DAEMON :: %s" % (str(e)))
        else:
            try:
                self.client = from_env()
            except Exception as e:
                raise Exception("ERROR CONNECTING TO LOCAL DAEMON :: %s" % (str(e)))


    def addContainer(self, container: DockerContainer):
        self.containers.append(container)

    def findContainers(self, service_name: str) -> List[DockerContainer]:
        return [c for c in self.containers if c.service_name == service_name]
    
    def addContainersFromJson(self, data: List[Dict[str, str]]):
        for con in data:
            _con = DockerContainer.from_json(con, self.client)
            self.containers.append(_con)

    def allPassing(self) -> NightcapDockerStatus:
        try:
            _failed = [f for f in self.containers if f.manditory == True and f.isPassing() == NightcapDockerStatus.FAILED]
            return NightcapDockerStatus.PASSING if _failed == [] else NightcapDockerStatus.FAILED
        except Exception as e:
            raise Exception("ERROR CHECKING CONTAINERS/IMAGES :: %s" % (str(e)))
        
    def restartMongo(self) -> NightcapDockerStatus:
        try:
            _mongo = [m for m in self.containers if m.container_name == "nightcapmongodb"]
            _mongo[0].container_restart()
        except Exception as e:
            raise Exception("ERROR RESTARTING MONGO CONTAINER :: %s" % (str(e)))
        
    def stopMongo(self) -> NightcapDockerStatus:
        try:
            _mongo = [m for m in self.containers if m.container_name == "nightcapmongodb"]
            _mongo[0].container_stop()
        except Exception as e:
            raise Exception("ERROR STOPPING MONGO CONTAINER :: %s" % (str(e)))
        
    def startMongo(self) -> NightcapDockerStatus:
        try:
            _mongo = [m for m in self.containers if m.container_name == "nightcapmongodb"]
            _mongo[0].container_start()
        except Exception as e:
            raise Exception("ERROR STARTING MONGO CONTAINER :: %s" % (str(e)))