# region Imports
from nightcapcore.command.command import Command
# endregion

class NightcapUpdaterRebootCommand(Command):
    def __init__(self) -> None:
        super().__init__()

    def execute(self) -> None:
        print("Reboot please")
        raise KeyboardInterrupt("Restarting")
