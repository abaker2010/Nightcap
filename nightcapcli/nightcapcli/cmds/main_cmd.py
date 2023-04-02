# region Imports
from nightcapcli.base.base_cmd import NightcapBaseCMD
from nightcapcli.mixins.cmd_parts.settings_cmdpart import SettingsCMDPart
from nightcapcli.mixins.cmd_parts.use_cmdpart import UseCMDPart
from nightcapcli.mixins.cmd_parts.shell_cmdpart import ShellCMDPart
from nightcapcli.mixins.cmd_parts.options_cmdpart import OptionsCMDPart
from nightcapcli.mixins.cmd_parts.projects_cmdpart import ProjectsCMDPart
# endregion

class NightcapMainCMD(NightcapBaseCMD, OptionsCMDPart, ProjectsCMDPart, \
                      SettingsCMDPart, UseCMDPart, ShellCMDPart):
    def __init__(
        self,
        selectedList,
        channelid: str = None,
    ) -> None:
        NightcapBaseCMD.__init__(self, selectedList, channelid)

        OptionsCMDPart.__init__(self, selectedList)
        ProjectsCMDPart.__init__(self, selectedList)

        SettingsCMDPart.__init__(self, channelid)
        UseCMDPart.__init__(self, selectedList)
        ShellCMDPart.__init__(self)
        

    def do_exit(self, line) -> bool:
        if len(self.selectedList) == 0:
            return True
        else:
            self.selectedList.pop()
            NightcapMainCMD.__init__(self, self.selectedList, self.channelid)
    