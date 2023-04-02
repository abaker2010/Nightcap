# region Imports
from nightcapcore.invoker import Invoker
from nightcappackages.classes.commands import NightcapRestoreHelper, NightcapBackupCommand
from nightcappackages.classes.helpers import NightcapCleanHelper
from nightcapcli.base import NightcapBaseCMD
# endregion

class NightcapBackupsCMD(NightcapBaseCMD):
    def __init__(self, selectedList: list, channelid):
        NightcapBaseCMD.__init__(self, selectedList, channelid=channelid)

    # region Backup
    def help_backup(self) -> None:
        self.printer.help("Backup your instance of the NightCAP program")
        self.printer.help("useage: backup <output location>")

    def do_backup(self, line) -> None:
        try:
            _backup_invoker = Invoker()
            _backup_invoker.set_on_start(NightcapBackupCommand(line))
            _backup_invoker.execute()
        except Exception as e:
            self.printer.print_error(e)
    # endregion

    # region Restore
    def help_restore(self) -> None:
        self.printer.help("Restore your instance of the NightCAP program from a backup")
        self.printer.help("useage: restore <output location>.ncb")

    def do_restore(self, line) -> None:
        NightcapRestoreHelper(str(line)).restore()
    # endregion

    def do_clean(self, line) -> None:
        NightcapCleanHelper().clean()
