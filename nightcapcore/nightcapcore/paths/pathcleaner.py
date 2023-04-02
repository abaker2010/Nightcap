
# region Imports
import os
# endregion

class NightcapPathCleaner(object):
    """

    This class is used to clean the system paths

    ...

    Attributes
    ----------
        cwd: -> str
            The currect dir

    Methods
    -------
        Accessible
        -------
            combine_with_base(self, path: str, paths: list = []): -> str
                this will combime the programs current path with the needed path for running packages

    """

    # region Init
    def __init__(self, cwd: str) -> None:
        super().__init__()
        self.cwd = cwd

    # endregion

    # region Combine with base
    def combine_with_base(self, path: str, paths: list = []) -> str:
        _cleaned_list = list(map(lambda v: str(v), paths))
        return os.sep.join([self.cwd, path, os.sep.join(_cleaned_list)])

    # endregion

    # region Combine with base for import
    def import_combine_with_base(self, path: str, paths: list = []) -> str:
        _cleaned_list = list(map(lambda v: str(v), paths))
        return ".".join(["nightcappackages", path, ".".join(_cleaned_list)])

    # endregion