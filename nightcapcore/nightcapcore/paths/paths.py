
# region Imports
import os
from .pathsenum import NightcapPathsEnum
from .pathcleaner import NightcapPathCleaner

# endregion


class NightcapPaths(NightcapPathCleaner):
    """

    This class is used to get the nightcap specific paths

    ...

    Methods
    -------
        Accessible
        -------

            generate_path(self, path: NightcapPathsEnum, pathextra: list = []): -> str
                get nightcap specific path

    """

    # region Init
    def __init__(self) -> None:
        """Paths for the Nightcap project"""
        NightcapPathCleaner.__init__(
            self, os.path.dirname(__file__).replace((os.sep + "paths"), "")
        )

    # endregion

    # region Generate Path
    def generate_path(self, path: NightcapPathsEnum, pathextra: list = []) -> str:
        try:
            return self.combine_with_base(path.value, pathextra)
        except Exception as e:
            raise e

    # endregion
