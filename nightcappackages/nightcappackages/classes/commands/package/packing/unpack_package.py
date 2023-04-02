import os
import json
import shutil
from nightcapcore.printers import Printer
from nightcapcore.package.package import Package
from nightcapcore.command.command import Command

class NightcapPackageUnpackerCommand(Command):
    # region Init
    def __init__(self, path: str = None, tmp_path: str = None) -> None:
        super().__init__()
        self.path = path
        self.pkg = None
        self.printer = Printer()
        self.tmp_path = tmp_path
    # endregion
    
    # region Execute
    def execute(self) -> Package:
        #unpacking and preparing file system for install
        try:
            _path = os.path.join(self.tmp_path, 'ncp_installer')
            self.printer.print_underlined_header("Unpacking Package")
            shutil.copyfile(self.path, f"{_path}.ncp")
            shutil.unpack_archive(
                f"{_path}.ncp", f"{_path}/", "zip"
            )

            self.printer.print_formatted_check("Unpacked")
            
            _base_path = ""
            for root, dirs, files in os.walk(f"{_path}"):
                for name in dirs:
                    if "src" not in name:
                        _base_path = os.path.join(root, name)
            
                with open(os.path.join(_base_path, "package_info.json")) as json_file:
                    _data = json.load(json_file)

                return Package(data=_data)
        except FileNotFoundError as nf:
            raise nf
        except Exception as e:
            raise e
    #endregion