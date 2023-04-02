from abc import ABC, abstractmethod

class VirtualEnv_Delete(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def delete(self):
        raise NotImplementedError