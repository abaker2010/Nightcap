# region Imports
from docker.errors import DockerException
from nightcapcore.command.command import Command
from nightcapcore.printers import Printer
from nightcapcore.configuration import NightcapCLIConfiguration
from nightcapcore.legal import Legal
from nightcapcore.menus.connection_controller_menu import NightcapConnectionControllerMenu
# endregion


class NightcapBootChecks(Command):
    """

    This class is used to as a wrapper for the entry process to the program

    ...

    Attributes
    ----------

        conf: -> NightcapCLIConfiguration
            this allows us to use the main configuration of the program

        printer: -> Printer
            allows us to print to the command line

        mongo_server = None


    Methods
    -------
        Accessible
        -------
            agreements(self): -> bool
                asks the user to agree to the terms of usage and conduct

            banner(self): -> None
                easier to access banner

    """

    def __init__(self) -> None:
        super().__init__()
        

    def execute(self) -> bool:
        _printer = Printer()
        _conf = NightcapCLIConfiguration()
        
        try:
            _legal = Legal()
            
            if _legal.check_legal():
                _docker_configer = NightcapConnectionControllerMenu()
                if(_conf.isDaemon == False):
                    if _docker_configer.change_configuration_no_daemon():
                        return True
                else:
                    if _docker_configer.change_configuration_with_daemon():
                        return True

            else:
                raise Exception("ERROR WITH ACCEPTING ULA")

        except DockerException as de:
            _printer.print_error(
                Exception("Error connecting to Docker Container(s) Please Reconfigure.")
            )
            _printer.print_error(de)
            _now = _printer.input(
                "Would you like to reconfigure now? (Y/n)", defaultReturn=True
            )
            return False
        except Exception as e:
            # _printer.print_error("ERROR REACHING DOCKER STUFF COULD FIX HERE :: %s" % (str(e)))
            # if _now:
            #     NightcapIPAddressHelper(_conf).change_connection_only()
            #     self.execute()
            # else:
            #     return False
            raise e
