# region Imports
from colorama import Fore
from nightcapcli.base.base_cmd import NightcapBaseCMD
# endregion

class NightcapMongoNetworkSettingsCMD(NightcapBaseCMD):
    """
    (User CLI Object)

    This class is used to control the Mongo Network Settings (This is a child cmd)

    ...

    Attributes
    ----------
        network: -> str
            Mainly used for the init of the NightcapBaseCMD which creates the needed view for the users display

        Other attrs that are inherited from the NightcapBaseCMD class

    Methods
    -------
        Accessible
        -------
            help_config(self): -> None
                Override for the configurations help option

            do_config(self, line): -> None
                Allows the user to set configurations for the Mongo Network Configurations

            help_ip(self):
                Override for the ips help command

            do_ip(self, line):
                Allows the user to set a new IP addres. ip <addr>

            help_port(self):
                Override for the ports help command

            do_port(self, line):
                Allows the user to set a new Port. port <port>

        None Accessible
        -------
            _isvalidIPAddress(self, IP): -> bool
                Returns a bool based on if the input was an IP address or not

    """

    # region Init
    def __init__(self, networkopt: str = 'database') -> None:
        self.network = ""
        if networkopt.lower() == "database":
            NightcapBaseCMD.__init__(self, ["settings", "database"])
            self.network = "MONGOSERVER"
        elif networkopt.lower() == "web":
            NightcapBaseCMD.__init__(self, ["settings", "web"])
            self.network = "REPORTINGSERVER"
        else:
            raise Exception("Invalid option: Please use web or database")

    # endregion

    # region Config
    def help_config(self) -> None:
        self.printer.help("Shows current configuration")

    def do_config(self, line) -> None:
        self.printer.print_underlined_header("CURRENT CONFIG")
        self.printer.print_formatted_other(
            "IP",
            self.config.config[self.network]["ip"],
            leadingTab=2,
            optionalTextColor=Fore.MAGENTA,
        )
        self.printer.print_formatted_other(
            "Port",
            self.config.config[self.network]["port"],
            endingBreaks=1,
            leadingTab=2,
            optionalTextColor=Fore.MAGENTA,
        )

    # endregion

    # region Is IP Valid
    def _isvalidIPAddress(self, IP) -> bool:
        """
        :type IP: str
        :rtype: str
        """

        def isIPv4(s):
            try:
                return str(int(s)) == s and 0 <= int(s) <= 255
            except:
                return False

        def isIPv6(s):
            if len(s) > 4:
                return False
            try:
                return int(s, 16) >= 0 and s[0] != "-"
            except:
                return False

        if IP.count(".") == 3 and all(isIPv4(i) for i in IP.split(".")):
            return True
        if IP.count(":") == 7 and all(isIPv6(i) for i in IP.split(":")):
            return True
        return False

    # endregion

    # region IP
    def help_ip(self) -> None:
        self.printer.help("Sets a new IP Address", "ip [IP Address]")

    def do_ip(self, line) -> None:
        print("Set IP")
        try:
            print("Change IP address for mongo server")
            if str(line).lower() == "localhost":
                self.config.config.set(self.network, "ip", "127.0.0.1")
                self.config.save()
            elif self._isvalidIPAddress(line):
                self.config.config.set(self.network, "ip", line)
                self.config.save()
            else:
                self.printer.print_error(
                    Exception(
                        "Error with setting IP Address { %s }, please try again" % line
                    )
                )
        except Exception as e:
            self.printer.print_error(e)

    # endregion

    # region Port
    def help_port(self) -> None:
        self.printer.help("Sets a new Port Number", "port [1-65535]")

    def do_port(self, line) -> None:
        print("Set port")
        try:
            port = int(line)
            if 1 <= port <= 65535:
                self.config.config.set(self.network, "port", line)
                self.config.save()
            else:
                raise ValueError
        except ValueError:
            self.printer.print_error(
                Exception(
                    "Error with setting Port { %s }. Expected range 1 - 65535, please try again"
                    % line
                )
            )
    # endregion