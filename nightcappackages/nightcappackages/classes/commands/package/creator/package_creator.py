# import os
# from bson import json_util
# from nightcapcore.command.command import Command
# from nightcapcore.printers.print import Printer
# from nightcapcore.package import Package
# from nightcapcore.helpers import NightcapJSONEncoder

# class NightcapPackageCreatorCommand(Command):

#     def __init__(self, package: Package) -> None:
#         super().__init__()
#         self.printer = Printer()
#         self.package = package

#     def execute(self) -> str:
#         self.printer.print_underlined_header("Generating package_info.json..")
#         try:
#             _json_data = json_util.dumps(self.package, cls=NightcapJSONEncoder)
#             self.printer.print_formatted_additional("Data Prepared...")

#             _package_tmp_path = f"/tmp/nightcap/{self.package.package_information.package_name}"
#             if os.path.isdir(_package_tmp_path) == False:
#                 os.makedirs(_package_tmp_path)

#             with open(f"{_package_tmp_path}/package_info.json", "w+") as file:
#                 file.write(_json_data)

#             self.printer.print_formatted_additional(
#                 "Package_info.json Path", optionaltext=f"{_package_tmp_path}/package_info.json"
#             )
            
#             return _package_tmp_path
#         except Exception as e:
#             raise e    