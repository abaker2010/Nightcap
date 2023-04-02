from typing import Callable, Any
from abc import ABC, abstractmethod

class Validate(ABC):

    @abstractmethod
    def validate(self, data: Any) -> bool:
        raise NotImplementedError