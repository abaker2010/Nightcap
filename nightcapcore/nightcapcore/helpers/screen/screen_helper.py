
# region Imports
import os
import platform
# endregion

class ScreenHelper(object):
    """

    This class is used to help with screen actions

    ...

    Methods
    -------
        Accessible
        -------
            clearScr(self): -> None
                Will clear the screen visible to the user

    """

    # region Init
    def __init__(self) -> None:
        super().__init__()

    # endregion

    # region Clear Screen
    def clearScr(self) -> None:
        if platform.system() == "windows":
            os.system("cls")
        else:
            os.system("clear")
    # endregion

    #region Terminal Size
    def terminalSize(self) -> os.terminal_size:
        return os.get_terminal_size()
    #endregion
