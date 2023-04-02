from nightcapcli.mixins.cmd_parts.base import CMDPartBase
from nightcapcore import ScreenHelper, NightcapBanner

class BannerCMDPart(CMDPartBase):
    def __init__(self) -> None:
        super().__init__()

    def do_banner(self, line):
        ScreenHelper().clearScr()
        NightcapBanner().Banner()