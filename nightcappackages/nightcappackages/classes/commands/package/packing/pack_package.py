import os
import json
import hashlib
import shutil
from pathlib import Path
import traceback
from nightcapcore.command.command import Command
from nightcapcore.hashing.hash import NightcapHash
from nightcapcore.helpers.json.encoder import NightcapJSONEncoder
from nightcapcore.package import Package
from nightcapcore.printers.print import Printer

class NightcapPackagePackerCommand(Command):
    def __init__(self, path: str = None) -> None:
        super().__init__()
        self.path = path
        self.printer = Printer()

    # region make archive
    def make_archive(self, source, destination) -> None:
        base = os.path.basename(destination)
        name = base.split(".")[0]
        format = base.split(".")[1]
        archive_from = os.path.dirname(source)
        archive_to = os.path.basename(source.strip(os.sep))
        shutil.make_archive(name, format, archive_from, archive_to)
        shutil.move("%s.%s" % (name, format), destination)

    # endregion
    
    def execute(self) -> dict:
        try:

            with open(os.path.join(self.path, "package_info.json")) as json_file:
                data = json.load(json_file)

            _package:Package = Package(data=data)
            package_name = _package.package_information.package_name
            package_module = _package.package_for.module
            package_submodule = _package.package_for.submodule

            hash = NightcapHash().hash_dict(data)
            print(f"Hash {hash}")
            _package.id = hash

            print(_package.report_design.title)

            _out_file = (
                package_module
                + "-"
                + package_submodule
                + "-"
                + package_name
                + "-"
                + str(_package.package_information.version).replace(".", "-")
            )
            
            _base = os.path.join(Path(self.path).parent, _out_file)

            with open(os.path.join(self.path, "package_info.json"), "w") as outfile:
                json.dump(_package, outfile, cls=NightcapJSONEncoder)

            self.printer.print_underlined_header("Trying to sign package")
            self.printer.print_formatted_additional("Please wait...")
            self.printer.print_formatted_additional(
                "Path to be used", optionaltext=self.path
            )
            self.printer.print_formatted_additional(
                "Package Being Created", optionaltext=_out_file + ".ncp"
            )

            self.make_archive(self.path, str(_base) + ".zip")
            os.rename(str(_base) + ".zip", str(_base) + ".ncp")

            with open(str(_base) + ".ncp", "rb") as f:
                file_hash = hashlib.md5()
                chunk = f.read(8192)
                while chunk:
                    file_hash.update(chunk)
                    chunk = f.read(8192)
            self.printer.print_formatted_check("Done", endingBreaks=1)

        except Exception as e:
            print(traceback.print_exc())
            print(e)