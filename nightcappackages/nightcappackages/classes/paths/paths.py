# region Imports
import os
from nightcapcore import NightcapPathCleaner
from nightcappackages.classes.paths.pathsenum import NightcapPackagesPathsEnum
# endregion

class NightcapPackagesPaths(NightcapPathCleaner):
    """

    This class is used to generate package paths

    ...

    Methods
    -------
        Accessible
        -------
            generate_path(self, path: NightcapPackagesPathsEnum, pathextra: list = []): -> str
                returns the path needed to run the installed package

    """

    # region Init
    def __init__(self):
        """Paths for the Nightcap project"""
        NightcapPathCleaner.__init__(
            self,
            os.path.dirname(__file__)
            .replace((os.sep + "paths"), "")
            .replace((os.sep + "classes"), ""),
        )

    # endregion

    # region Generate Path
    def generate_path(self, path: NightcapPackagesPathsEnum, pathextra: list = []):
        try:
            return self.combine_with_base(path.value, pathextra)
        except Exception as e:
            return e

    # endregion

    # region Generate Import Path
    def generate_import_path(self, path: NightcapPackagesPathsEnum, pathextra: list = []):
        try:
            return self.import_combine_with_base(path.value, pathextra)
        except Exception as e:
            return e
    # endregion
