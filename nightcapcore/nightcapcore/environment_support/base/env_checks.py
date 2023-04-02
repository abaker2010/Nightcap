from abc import ABC, abstractmethod

class VirtualEnv_Checks(ABC):
    
    @abstractmethod
    def check_env(self):
        raise NotImplementedError

    @abstractmethod
    def check_version_installed(self):
        raise NotImplementedError
    
    @abstractmethod
    def check_version_downloadable(self):
        raise NotImplementedError