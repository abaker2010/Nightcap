
# region Imports
import os
from colorama import Style, Fore
from nightcapcore.helpers.screen import ScreenHelper
from nightcapcore.printers.print import Printer
from nightcapcore.banner.nightcap_banner import NightcapBanner
from nightcapcore.helpers.screen.screen_helper import ScreenHelper
from nightcapcore.docker.docker_status import NightcapDockerStatus
from nightcapcore.configuration import NightcapCLIConfiguration


DEVNULL = open(os.devnull, "wb")
# endregion

class NightcapConnectionControllerMenu(object):
 
    def __init__(self) -> None:
        super().__init__()
        self.conf = NightcapCLIConfiguration()
        self.printer = Printer()

    # region Change Config With Out Daemon
    def change_configuration_no_daemon(self):
        ScreenHelper().clearScr()
        NightcapBanner().Banner()

        # region Print warnings for Docker/MongoDB not available
        if self.conf.mongoAvailable == False:
            self.printer.print_error("Unable to connect to MongoDB Instance", endingBreaks=0)
            self.printer.print_error("Please check MongoDB config and reconnect", endingBreaks=0)

        self.printer.print_underlined_header("Current Mongo Settings")
        self.printer.print_formatted_additional(
            text="IP", optionaltext=self.conf.mongo_ip
        )
        self.printer.print_formatted_additional(
            text="Port",
            optionaltext=self.conf.mongo_port,
        )
        # endregion

        # region Printing Option List
        self.printer.print_underlined_header("Please Select an option")
        self.printer.print_formatted_additional(
            text="Change Settings",
            optionaltext="CS",
            leadingTab=2,
            optionalTextColor=Fore.MAGENTA,
        )
        self.printer.print_formatted_additional(
            text="Connect",
            optionaltext="C",
            leadingTab=2,
            optionalTextColor=Fore.MAGENTA,
        )
        self.printer.print_formatted_additional(
            text="Exit",
            optionaltext="E",
            leadingTab=2,
            optionalTextColor=Fore.MAGENTA,
            endingBreaks=1,
        )
        # endregion

        # region User Selection Controls
        _selection = self.printer.input_return_only("Choice: ", defaultReturn="", leadingBreaks=2)
        if _selection != "":
            if _selection.strip().lower() == "cs":
                print("Change Settings")
                self._change_mogo_settings()
                self.change_configuration_no_daemon()
            elif _selection.strip().lower() == "c":
                if self.conf.mongoAvailable:
                    return True
                else:
                    self.change_configuration_no_daemon()
            elif _selection.strip().lower() == "e":
                ScreenHelper().clearScr()
                raise KeyboardInterrupt()
            else:
                ScreenHelper().clearScr()
                self.printer.print_error(Exception("Selection not allowed. Please try again."))
                self.change_configuration_no_daemon()
        else:
            ScreenHelper().clearScr()
            self.printer.print_error(Exception("Selection not allowed. Please try again."))
            self.change_configuration_no_daemon()

        return True
        # endregion
    # endregion

    # region Change Config With Daemon
    def change_configuration_with_daemon(self) -> bool:
        ScreenHelper().clearScr()
        NightcapBanner().Banner()
        self.printer.print_underlined_header(" - Docker Instance - ", leadingText='')

        # region Print warnings for Docker/MongoDB not available
        if self.conf.dockerAvailable == False:
            self.printer.print_error("Unable to connect to Docker Daemon", endingBreaks=0)
            self.printer.print_error("Please check Docker config and reconnect", endingBreaks=0)
        
        if self.conf.mongoAvailable == False:
            self.printer.print_error("Unable to connect to MongoDB Instance", endingBreaks=0)
            self.printer.print_error("Please check MongoDB config and reconnect", endingBreaks=0)
        # endregion

        # region Printing Network Settings
        self.printer.print_underlined_header("Current Network Settings")
        self.printer.print_formatted_additional(
            text="IP", optionaltext=self.conf.mongo_ip
        )
        self.printer.print_formatted_additional(
            text="Port",
            optionaltext=self.conf.mongo_port,
        )
        self.printer.print_formatted_additional(
            text="Remote Daemon",
            optionaltext=self.conf.isDaemon,
        )
        self.printer.print_formatted_additional(
            text="Shutdown Mongo (On Exit)",
            optionaltext=self.conf.mongo_shutdown,
            endingBreaks=1,
        )
        # endregion 

        # region Printing Docker Settings
        self.printer.print_underlined_header("Current Docker Settings")

        self.printer.print_formatted_additional(
            "IP", self.conf.docker_ip
        )
        self.printer.print_formatted_additional(
            "Port", self.conf.docker_port
        )
        self.printer.print_formatted_additional(
            "Is Daemon", self.conf.isDaemon
        )
        # endregion

        # region Print Docker Manager Information
        for container in self.conf.dockerManager.containers:
            self.printer.print_underlined_header_undecorated(container.service_name, leadingTab=2)
            self.printer.item_2(
                text="Image",
                optionalText=str(container.image_exists().value).capitalize(),
                leadingTab=3,
            )
            self.printer.item_2(
                text="Container",
                optionalText=str(container.container_status().value).capitalize(),
                leadingTab=3,
            )
            self.printer.item_2(
                text="Manditory",
                optionalText=str(container.isManditory().value).capitalize(),
                leadingTab=3,
            )
            self.printer.item_2(
                text="Passing",
                optionalText=str(container.isPassing().value).capitalize(),
                leadingTab=3,
                endingBreaks=1,
            )
        # endregion

        # region Printing Option List
        self.printer.print_underlined_header("Please Select an option")
        self.printer.print_formatted_additional(
            text="(Re)Start",
            optionaltext="R | S",
            leadingTab=2,
            optionalTextColor=Fore.MAGENTA,
        )
        self.printer.print_formatted_additional(
            text="Change Settings",
            optionaltext="CS",
            leadingTab=2,
            optionalTextColor=Fore.MAGENTA,
        )
        self.printer.print_formatted_additional(
            text="Connect",
            optionaltext="C",
            leadingTab=2,
            optionalTextColor=Fore.MAGENTA,
        )
        self.printer.print_formatted_additional(
            text="Exit",
            optionaltext="E",
            leadingTab=2,
            optionalTextColor=Fore.MAGENTA,
            endingBreaks=1,
        )
        # endregion

        # region User Selection Controls
        _selection = self.printer.input_return_only("Choice: ", defaultReturn="", leadingBreaks=2)

        if _selection != "":
            if _selection.strip().lower() == "cs":
                self._change_mogo_settings()
                self.change_configuration_with_daemon()
            elif _selection.strip().lower() == "c":
                if self.conf.dockerAvailable == False or self.conf.mongoAvailable == False or \
                    self.conf.dockerManager.allPassing() != NightcapDockerStatus.PASSING:
                        self.printer.print_error(Exception("Mongo container needs to be running"))
                        self.change_configuration_with_daemon()
                else:
                    return True

            elif _selection.strip().lower() == "st":
                _selection2 = self.printer.input_return_only("Would you like to stop both containers? (M/U/A/E)")

                if str(_selection2).lower() == "m":
                    self.printer.print_formatted_additional("Stopping container...")
                    self.conf.dockerManager.stopMongo()
                    ScreenHelper().clearScr()
                    self.change_configuration_with_daemon()

            elif _selection.strip().lower() == "s":
                _selection2 = self.printer.input_return_only("Would you like to start both containers? (M/U/A/E)")

                if str(_selection2).lower() == "m":
                    self.printer.print_formatted_additional("Starting container...")
                    self.conf.dockerManager.startMongo()
                    ScreenHelper().clearScr()
                    self.change_configuration_with_daemon()
                #     _mstatus = self.conf.dockerClient.container_start()

                if str(_selection2).lower() == "u":
                    pass
                # if str(_selection2).lower() == "a":
                    
                #     _mstatus = self.conf.dockerClient.container_start()

                if str(_selection2).lower() == "u":
                    pass
                # if str(_selection2).lower() == "e":
                #     pass

                if str(_selection2).lower() == "e":
                    ScreenHelper().clearScr()
                    self.change_configuration_with_daemon()
            elif _selection.strip().lower() == "r":
                _selection2 = self.printer.input_return_only("Would you like to restart both containers? (M/U/A/E)")
                # _mstatus = self.conf.dockerClient.continer_restart()
                if str(_selection2).lower() == "m":
                    self.printer.print_formatted_additional("Restarting container...")
                    self.conf.dockerManager.restartMongo()

                self.change_configuration_with_daemon()
                # if _mstatus == None:
                #     ScreenHelper().clearScr()
                #     self.printer.print_error(Exception("Could not restart container. Some are missing."))
                #     self.change_configuration_dockerized()
                # pass
            elif _selection.strip().lower() == "e":
                ScreenHelper().clearScr()
                exit()
            else:
                ScreenHelper().clearScr()
                self.printer.print_error(Exception("Selection not allowed. Please try again."))
                self.change_configuration_with_daemon()
        else:
            ScreenHelper().clearScr()
            self.printer.print_error(Exception("Selection not allowed. Please try again."))
            self.change_configuration_with_daemon()

        return True
        # endregion
    # endregion

    # This needs to be moved at somepoint to another class
    def _change_mogo_settings(self):
        ScreenHelper().clearScr()
        _format = "%s\n\t%s\n"
        _header_format = "\n\t\t%s\n\t\t* %s *\n\t\t%s\n"

        _title = "Database Configuration"

        _header_lines = "*" * (len(_title)+4) 
        _header = _header_format % (_header_lines, _title, _header_lines)
        
        _body = "Change the IP/Port to connect to for the back end. \
                \n\tPress CRTL+C to exit and keep previous config."

        intro = (_format % (_header, _body))
        print(intro)
        try:
            self.printer.print_underlined_header("Changing Mongo Config")
            _current_ip = self.conf.mongo_ip
            _currnet_port = self.conf.mongo_port
            _ip = input(Fore.LIGHTGREEN_EX + f"\t\tNew IP Address ({_current_ip}): " + Style.RESET_ALL).lower()
            _port = input(Fore.LIGHTGREEN_EX +f"\t\tNew Port ({_currnet_port}): " + Style.RESET_ALL).lower()
            try:
                self.conf.config.set("MONGOSERVER", "ip", str(_ip))
                self.conf.config.set("MONGOSERVER", "port", str(_port))
                self.conf.save()
            except Exception as e:
                self.printer.print_error(e)
                return False
            return True
        except KeyboardInterrupt as e:
            ScreenHelper().clearScr()
            self.printer.print_error(Exception("User terminated configuration"))
            return False