
# region Imports
from colorama import Fore, Style
from nightcapcore import (
    ScreenHelper,
    Printer,
    NightcapCLIConfiguration,
    NightcapBanner)

# endregion


class Legal(object):
    """ Handles the legal header """

    def __init__(self) -> None:
        super().__init__()
        self.conf = NightcapCLIConfiguration()
        self.printer = Printer()

    def termsAndConditions(self) -> None:
        print(Fore.LIGHTYELLOW_EX + "\n\tI shall not use nightcap to:")
        print("\t-----------------------------\n")
        print("\t\t(i) inspect or, display or distribute any content that")
        print(
            "\t\t\tinfringes any trademark, trade secret, copyright or other proprietary"
        )
        print(
            "\t\t\tor intellectual property rights of any person or company; \n\n"
            + Style.RESET_ALL
        )

    def check_legal(self):
        """Legal agreement the at the user must accept to use the program"""
        while not self.conf.config.getboolean("NIGHTCAPCORE", "agreement"):
            ScreenHelper().clearScr()
            NightcapBanner().Banner()
            self.termsAndConditions()
            agree = self.printer.input(
                "You must agree to our terms and conditions first (y/N)"
            )

            if agree:
                self.conf.config.set("NIGHTCAPCORE", "agreement", True)
                self.conf.save()
                ScreenHelper().clearScr()
                return True
        return True