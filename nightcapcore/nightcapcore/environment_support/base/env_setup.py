from abc import ABC, abstractmethod

class VirtualEnv_Setup(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def create_env(self):
        raise NotImplementedError
    
    # @abstractmethod
    # def check_env(self):
    #     raise NotImplementedError

    # @abstractmethod
    # def check_version_installed(self):
    #     raise NotImplementedError
    
    # @abstractmethod
    # def check_version_downloadable(self):
    #     raise NotImplementedError

    @abstractmethod
    def install_version(self):
        raise NotImplementedError
    
    @abstractmethod
    def update_new_env(self):
        raise NotImplementedError