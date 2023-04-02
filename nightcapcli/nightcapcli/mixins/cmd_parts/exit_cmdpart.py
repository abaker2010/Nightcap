from nightcapcli.mixins.cmd_parts.base import CMDPartBase

class ExitCMDPart(CMDPartBase):
    def __init__(self) -> None:
        super().__init__()

    def do_exit(self, line):
        return True