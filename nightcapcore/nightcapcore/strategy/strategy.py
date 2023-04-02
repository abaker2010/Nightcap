from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


class Strategy(ABC):
    """
    The Strategy interface declares operations common to all supported versions
    of some algorithm.

    The Context uses this interface to call the algorithm defined by Concrete
    Strategies.
    """

    @abstractmethod
    def execute(self, *arg, **kwargs):
        pass
