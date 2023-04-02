
from nightcapcli.base.base_cmd import NightcapBaseCMD
from nightcapcli.cmds.settings.backup_cmd import NightcapBackupsCMD
from nightcapcli.cmds.settings.network_cmd import NightcapNetworkCMD


class NightcapSystemCMD(NightcapBaseCMD):
    def __init__(self, channelid:str = None) -> None:
        NightcapBaseCMD.__init__(self, ["settings", "system"], channelid)


     # region Backups
    def help_backups(self) -> None:
        self.printer.help("Backup/Restore options for your instance of the NightCAP DB")

    def do_backups(self, line) -> None:
        NightcapBackupsCMD(["settings", "system", "backups"], "backups-main").cmdloop()
    # endregion

        # region Networking Options
    def help_network(self) -> None:
        self.printer.help("Select the protocol to use for requests")

    def do_network(self, line) -> None:
        NightcapNetworkCMD("networking-main").cmdloop()
    # endregion
    
    # region Exit
    def do_exit(self, line) -> bool:
        return True
    # endregion
