
# region Imports
from random import randint
from art import *
from colorama import Style
from nightcapcore.colors import NightcapColors
from nightcapcore.configuration.configuration import NightcapCLIConfiguration
# endregion

class NightcapBanner(object):
    """

    This class is used create the banner for the cli

    ...

    Attributes
    ----------
        build_version: -> str
            build version of the program

        build_number: -> str
            build number of the program

    Methods
    -------
        Accessible
        -------
            Banner(self, rand: bool = True): -> None
                Prints the banner to the console

        None Accessible
        -------
            _randomColor(self): -> const
                returns a colorama color

    """

    # region Init
    def __init__(self):
        self.conf = NightcapCLIConfiguration()

    # endregion

    # region Random Color
    def _randomColor(self) -> str:
        random = randint(0, 11)
        return NightcapColors().randomColor(random)

    # endregion

    # region Banner
    def Banner(self, rand: bool = True) -> None:
        rcolor = None
        rcolor2 = self._randomColor()
        rcolor3 = self._randomColor()
        if rand == True:
            rcolor = self._randomColor()
        else:
            rcolor = NightcapColors().randomColor(0)

        print(rcolor)
        Art = text2art("Nightcap", font="rnd-medium")
        sart = Art.splitlines()
        for l in sart:
            print(l.center(125, " "))
        print("\n\t", "=" * 100)
        print("\t=", rcolor3, "Created By: Aaron Baker".center(96, " "), rcolor, "=")
        print("\t=", " " * 98, "=")
        try:
            version_string = rcolor + "Version ~ " + rcolor2 + str(self.conf.versionNumber)
            build_number_string = rcolor + "Build ~ " + rcolor2 + str(self.conf.buildNumber)
            branch_string = (
                rcolor + "Branch ~ " + rcolor2 + ("Main" if self.conf.mainbranch else "Dev")
            )
            print(
                "\t=",
                rcolor2,
                ("%s" % (branch_string)).center(106, " "),
                rcolor,
                "=",
            )
            print("\t=", " " * 98, "=")
            print(
                "\t=",
                rcolor2,
                ("%s\t\t%s" % (build_number_string, version_string)).center(107, " "),
                rcolor,
                "=",
            )
        except Exception as e:
            print(str(e))
        print("\t", "=" * 100, Style.RESET_ALL, "\n")
        return

    # endregion
