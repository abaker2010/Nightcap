from __future__ import annotations
from abc import ABC, abstractmethod


class Command(ABC):
    """

    The Command interface declares a method for executing a command.

    ...

    Methods
    -------
        Accessible
        -------
            @abstractmethod
            execute(self) -> None:
                Execute command

    """

    @abstractmethod
    def execute(self) -> dict:
        pass
