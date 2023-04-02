from abc import ABC, abstractmethod

class VirtualEnv_Init(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def install_requirements(self):
        raise NotImplementedError
        