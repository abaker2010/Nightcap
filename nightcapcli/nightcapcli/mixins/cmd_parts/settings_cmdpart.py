from nightcapcore import ScreenHelper
from nightcapcli.cmds.settings.settings_cmd import NightcapSettingsCMD
from nightcapcli.mixins.cmd_parts.base import CMDPartBase

class SettingsCMDPart(CMDPartBase):
    def __init__(self, channelid: str = None) -> None:
        super().__init__()
        self.channelid = channelid

    # region Settings
    def do_settings(self, line) -> None:
        ScreenHelper().clearScr()
        NightcapSettingsCMD(self.channelid).cmdloop()
    # endregion