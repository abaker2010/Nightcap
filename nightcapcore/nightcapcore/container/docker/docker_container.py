from __future__ import annotations
from docker.client import DockerClient
from docker.errors import ImageLoadError, APIError
from docker.models.containers import Container as DContainer
from nightcapcore.container.base.container import Container
from nightcapcore.docker.docker_status import NightcapDockerStatus

class DockerContainer(Container):
    def __init__(self, service_name: str = None, container_name: str = None, 
                 image_name: str = None, image_version: str = None, ip: str = None, 
                 port: str = None, username: str = None, password: str = None, 
                 shutdown_on_exit: bool = False, manditory: bool = False, dockerClient: DockerClient = None) -> None:
        super().__init__(service_name, container_name, image_name, 
                         image_version, ip, port, username, password, shutdown_on_exit, manditory)
        self.dockerClient = dockerClient
        self.container_id = None
        self.remote_image_data = None
        self.remote_container_data = None
        self.current_image_state:NightcapDockerStatus = None
        self.current_container_state:NightcapDockerStatus = None

    def isPassing(self) -> NightcapDockerStatus:
        try:
            if self.manditory:
                if self.current_container_state == NightcapDockerStatus.RUNNING:
                    if self.current_image_state == NightcapDockerStatus.EXISTS:
                        return NightcapDockerStatus.PASSING
                    else: 
                        return NightcapDockerStatus.FAILED
                else:
                    return NightcapDockerStatus.FAILED
            else:
                return NightcapDockerStatus.PASSING
        except Exception as e:
            raise Exception("ERROR CHECKING DOCKER STATUS ISPASSING :: %e" % (str(e)))

    def isManditory(self) -> NightcapDockerStatus:
        return NightcapDockerStatus.MANDITORY if self.manditory else NightcapDockerStatus.NOTMANDITORY

    def image_exists(self) -> NightcapDockerStatus: 
        try:
            self.remote_image_data = self.dockerClient.images.get(self.image_name)
            if self.remote_image_data == None:
                self.current_image_state = NightcapDockerStatus.MISSING
            else:
                self.current_image_state = NightcapDockerStatus.EXISTS
        except ImageLoadError as im:
            self.current_image_state = NightcapDockerStatus.MISSING
        except APIError as apierror:
            self.current_image_state = NightcapDockerStatus.MISSING
        except Exception as e:
            raise Exception("ERROR GETTING REMOTE IMAGE INFORMATION :: %s" % (str(e)))

        return self.current_image_state

    def container_status(self) -> NightcapDockerStatus:
        try:
            self.remote_container_data = self.dockerClient.api.containers(filters={"name": self.image_name})
            # print(self.remote_container_data)
            if self.remote_container_data == NightcapDockerStatus.MISSING:
                self.current_container_state = NightcapDockerStatus.MISSING
            elif self.remote_container_data != []:
                _container_data = self.remote_container_data[0].get('State')
                self.container_id = self.remote_container_data[0].get('Id')
                if _container_data == "created":
                    self.current_container_state = NightcapDockerStatus.EXISTS
                elif _container_data == "running":
                    self.current_container_state = NightcapDockerStatus.RUNNING
                elif _container_data == "exited":
                    self.current_container_state = NightcapDockerStatus.STOPPED
                elif _container_data == "paused":
                    self.current_container_state = NightcapDockerStatus.PAUSED
                else:
                    raise Exception("Container %s Status Needs Fixed!" % self.container_name)
            else:
                self.current_container_state = NightcapDockerStatus.MISSING
        except ImageLoadError as im:
            self.current_container_state = NightcapDockerStatus.MISSING
        except APIError as apierror:
            self.current_container_state = NightcapDockerStatus.MISSING
        except Exception as e:
            raise Exception("ERROR GETTING REMOTE CONTAINER INFORMATION :: %s" % (str(e)))
        
        return self.current_container_state
    
    def container_start(self) -> NightcapDockerStatus:
        try:
            _remote_container:DContainer = self.dockerClient.containers.get(self.container_id)
            if _remote_container != None:
                if _remote_container.status == NightcapDockerStatus.PAUSED.value:
                    self.dockerClient.api.unpause(_remote_container.attrs)
                elif _remote_container.status == NightcapDockerStatus.STOPPED.value:
                    self.dockerClient.api.start(_remote_container.attrs)
        
        except APIError as apierr:
            raise Exception("STARTING ERROR API :: %s" % (str(apierr)))

        except Exception as e:
            raise Exception("ERROR RESTARTING CONTAINER :: %s" % (str(e)))
        
    def container_stop(self) -> NightcapDockerStatus:
        try:
            _remote_container = self.dockerClient.containers.get(self.container_id)
            if _remote_container != None:
                self.dockerClient.api.pause(_remote_container.attrs)
        
        except APIError as apierr:
            raise Exception("STOPPING ERROR API :: %s" % (str(apierr)))

        except Exception as e:
            raise Exception("ERROR STOPPING CONTAINER :: %s" % (str(e)))
    
    def container_restart(self) -> NightcapDockerStatus:
        try:
            _remote_container = self.dockerClient.containers.get(self.container_id)
            if _remote_container != None:
                self.dockerClient.api.restart(_remote_container.attrs)
        
        except APIError as apierr:
            raise Exception("RESTARTING ERROR API :: %s" % (str(apierr)))

        except Exception as e:
            raise Exception("ERROR RESTARTING CONTAINER :: %s" % (str(e)))

    def from_json(jsonData: dict, dockerClient: DockerClient) -> DockerContainer:
        if "manditory" in jsonData:
            jsonData['manditory'] = True if str(jsonData["manditory"]).lower() == "true" else False
        return DockerContainer(**jsonData, dockerClient=dockerClient)