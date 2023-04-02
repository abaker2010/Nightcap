from __future__ import annotations

class Container(object):
    def __init__(self, service_name: str = None, container_name: str = None, 
                 image_name: str = None, image_version: str = None, 
                 ip: str = None, port: str = None, username: str = None, password: str = None,
                 shutdown_on_exit: bool = False, manditory: bool = False) -> None:
        
        # region General properties for building the container
        self.service_name = service_name
        self.container_name = container_name
        self.image_name = image_name
        self.image_version = image_version
        self.manditory = manditory
        # endregion

        # region Other informmation about the container
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

        self.shutdown_on_exit = shutdown_on_exit
        # endregion
        
    def from_json(self, jsonData: dict) -> Container:
        return Container(**jsonData)

    def to_json(self):
        return self.__dict__