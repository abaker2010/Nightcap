# region Imports
import urllib
import json
from nightcapcore import Printer
# endregion


class NightcapPackageVersionCheckHelper(object):
    # region Init
    def __init__(
        self,
        main: bool,
        cfgMain: bool,
        current_build: str,
        current_version: str,
        verbose: bool = False,
    ):
        self.tmpdir = None
        self.printer = Printer()
        self.isMainBranch = main
        self.configMainBranch = cfgMain
        self.build = current_build
        self.version = current_version

    # endregion

    def check(self) -> None:
        # return super().execute()
        self.printer.print_formatted_additional("Getting Remote Versions")
        _url = "https://raw.githubusercontent.com/abaker2010/NightCAPVersions/main/versions.json"

        try:
            r = urllib.request.urlopen(_url)
            status_code = r.getcode()

            if status_code == 200:
                _versions = json.load(r)

                _current_build = int(self.build)
                _current_version = int(self.version)

                if self.isMainBranch:
                    _remote_version = int(_versions["stable"]["version"])
                    _remote_build = int(_versions["stable"]["build"])
                else:
                    _remote_version = int(_versions["dev"]["version"])
                    _remote_build = int(_versions["dev"]["build"])

                if (
                    self.configMainBranch == self.isMainBranch
                    and _current_build == _remote_build
                    and _current_version == _remote_version
                ):
                    return (False, _remote_build, _remote_version)
                else:
                    return (True, _remote_build, _remote_version)

        except Exception as e:
            self.printer.print_error(Exception("Error getting versions.json"))
            self.printer.print_error(e)
