from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict

class ILangStrategy(ABC):
    """
    The Lang Strategy is developed for the interface of supporting different 
        languages. An example use of this interface is for integration of programming
        languages like ruby, perl, python, go, etc.

    Purpose:
        To be used for creation of the concrete object for the supporting language
    """

    @abstractmethod
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def exectue(self, *arg, **kwargs) -> Dict:
        """
        Purpose: 
            Execute the underlying method
        
        Returns:
            returns information about the outcome of the execution
        """
        pass

    @abstractmethod
    def information(self, *args, **kwargs) -> Dict:
        """
        Purpose:
            gives information about the Strategy

        Returns:
            returns the information about the strategy
        """
        pass


