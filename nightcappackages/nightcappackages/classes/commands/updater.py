# region Imports
import shutil
from colorama import Fore
from nightcapcore import Printer
from tqdm.auto import tqdm
import os
import shutil
import json
from nightcapcore.configuration.configuration import NightcapCLIConfiguration
from nightcapcore.command.command import Command
from nightcapcore.invoker.invoker import Invoker
from nightcapcore.helpers.tmp_files import NightcapTmpFiles
from nightcappackages.classes.commands.package import  NightcapPackageInstallerCommand, \
                    NightcapPackageUninstallerCommand, \
                    NightcapPackageUpdateDownloaderCommand
from nightcappackages.classes.helpers.check_version import NightcapPackageVersionCheckHelper
from nightcapcore.database.mongo.mongo_packages import MongoPackagesDatabase
# endregion


class NightcapPackageUpdaterCommand(Command):
    # region Init
    def __init__(
        self,
        main: bool,
        verbose: bool = False,
        force=False,
    ):
        self.currentDir = os.getcwd()
        self.updateFile = "update.ncb"
        self.isMainBranch = None
        self.printer = Printer()
        self.verbose = False
        self.config = NightcapCLIConfiguration()
        self.main = main
        self.verbose = verbose
        self.force = force

    # endregion

    # region Execute
    def execute(self) -> None:
        # self.updateCalled = True
        self.isMainBranch = self.main
        self.verbose = self.verbose
        try:
            self.printer.print_underlined_header(
                "Updating NightCAP", underline="*", endingBreaks=1, leadingText=""
            )
            if self.verbose == False:
                self.printer.print_header(leadingText="[-]", text="Please wait...")

            _available = tuple(
                NightcapPackageVersionCheckHelper(
                    self.isMainBranch,
                    self.config.mainbranch,
                    self.config.buildNumber,
                    self.config.versionNumber,
                ).check()
            )

            # reigon needs fixed

            if _available[0] == False and self.force == False:
                self.printer.print_formatted_check(
                    "Running the most current version", endingBreaks=1
                )
            else:
                self.printer.print_formatted_additional("Update Available")
                if self.force == False:
                    agree = self.printer.input("Would you like to update now? (Y/n)")
                else:
                    agree = True

                if agree:

                    if self.isMainBranch:
                        _url = (
                            "https://github.com/abaker2010/NightCAPVersions/raw/main/%s/%s/update.ncb"
                            % (str(_available[1]), str(_available[2]))
                        )
                    else:
                        _url = (
                            "https://github.com/abaker2010/NightCAPVersions/raw/main/%s/%s/update-dev.ncb"
                            % (str(_available[1]), str(_available[2]))
                        )
                    _tmpfile = NightcapTmpFiles()

                    try:
                        _tmpfile.create_folder()
                        print("\n")
                        invoker = Invoker()
                        invoker.set_on_start(
                            NightcapPackageUpdateDownloaderCommand(
                                _url, _tmpfile.tmp_dir
                            )
                        )
                        _updater = tuple(invoker.execute())
                        if _updater[0] == True:
                            self._update(str(_updater[1]), str(_updater[2]))

                    except Exception as e:
                        raise e
                    finally:
                        _tmpfile.clean_up()
                        pass

                    self.config.config.set(
                        "BUILD_DATA", "main_branch", str(self.isMainBranch)
                    )
                    self.config.config.set("BUILD_DATA", "build", _available[1])
                    self.config.config.set("BUILD_DATA", "version", _available[2])

                    self.config.buildNumber = _available[1]
                    self.config.versionNumber = _available[2]
                    self.config.mainbranch = _available[0]
            self.config.save()
            
            self.printer.print_formatted_check(
                "Update Complete",
                leadingColor=Fore.MAGENTA,
                leadingTab=1,
                leadingBreaks=2,
                titleColor=Fore.CYAN,
                endingBreaks=1,
            )
            # endregion

        except KeyboardInterrupt as e:
            self.printer.print_error(Exception("User Terminated"))
            # self.updateCalled = False
        except Exception as ee:
            self.printer.print_error(ee)
        finally:
            pass

    # region Update
    def _update(self, tmppath: str, filename: str):
        try:
            if ".ncb" in filename:

                name = os.path.basename(str(filename))
                new_name = name.replace(".ncb", ".zip")

                os.rename(os.path.join(tmppath, name), os.path.join(tmppath, new_name))

                shutil.unpack_archive(
                    os.path.join(tmppath, new_name), os.path.join(tmppath, "updater"), "zip"
                )
                shutil.unpack_archive(
                    os.path.join(tmppath, "updater", "installers.zip"),
                    os.path.join(tmppath, "updater", "installers"),
                    "zip",
                )

                _installers_path = os.path.join(tmppath, "updater", "installers")
                _r_paths = self._restore_installers_paths(_installers_path)

                description = Fore.LIGHTMAGENTA_EX + "\t[-] Installing  "

                for i in tqdm(range(len(_r_paths)), desc=description, ncols=100, unit="m"):
                    _r = _r_paths[i]

                    _new_name = str(_r["path"]).replace(".ncp", ".zip")

                    os.rename(str(_r["path"]), _new_name)

                    shutil.unpack_archive(
                        _new_name, os.path.join(tmppath, str(_r["name"])), "zip"
                    )

                    os.rename(_new_name, str(_r["path"]))

                    for root, dirs, files in os.walk(
                        os.path.join(tmppath, str(_r["name"])), topdown=False
                    ):
                        for name in files:
                            if name == "package_info.json":
                                with open(os.path.join(root, name)) as json_file:
                                    _package = json.load(json_file)

                                _pkexists = MongoPackagesDatabase().check_package_path(
                                    [
                                        _package["package_for"]["module"],
                                        _package["package_for"]["submodule"],
                                        _package["package_information"]["package_name"],
                                    ]
                                )

                                if _pkexists == False:
                                    invoker = Invoker()
                                    invoker.set_on_start(
                                        NightcapPackageInstallerCommand(str(_r["path"]))
                                    )
                                    invoker.execute()
                                else:

                                    _current_package = (
                                        MongoPackagesDatabase().get_package_config(
                                            [
                                                _package["package_for"]["module"],
                                                _package["package_for"]["submodule"],
                                                _package["package_information"][
                                                    "package_name"
                                                ],
                                            ]
                                        )
                                    )
                                    if (
                                        _current_package["package_information"]["version"]
                                        == _package["package_information"]["version"]
                                    ):
                                        pass
                                    else:
                                        invoker = Invoker()
                                        invoker.set_on_start(
                                            NightcapPackageUninstallerCommand(
                                                "/".join(
                                                    [
                                                        _package["package_for"]["module"],
                                                        _package["package_for"][
                                                            "submodule"
                                                        ],
                                                        _package["package_information"][
                                                            "package_name"
                                                        ],
                                                    ]
                                                ),
                                                True,
                                            )
                                        )
                                        invoker.execute()

                                        invoker.set_on_start(
                                            NightcapPackageInstallerCommand(str(_r["path"]))
                                        )
                                        invoker.execute()
                return True
            else:
                self.printer.print_error(
                    Exception("Please check the backup file. Inforrect file type used")
                )
                return False
        except Exception as installer_failure:
            raise installer_failure

    def _restore_installers_paths(self, location: str):
        _installers = []

        for root, dirs, files in os.walk(location):
            for file in files:
                if file.endswith(".ncp"):
                    _installers.append(
                        {
                            "name": file.replace(".ncp", ""),
                            "path": os.path.join(root, file),
                        }
                    )
        return _installers

    # endregion
