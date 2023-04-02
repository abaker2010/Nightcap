# region Imports
from nightcapcore.printers import Printer
from nightcapcore.command.command import Command
from nightcapcore.configuration.configuration import NightcapCLIConfiguration
# endregion

class NightcapShutdownChecks(Command):
    def __init__(self) -> None:
        super().__init__()
        self.printer = Printer()
        self.conf = NightcapCLIConfiguration()

    def execute(self) -> None:
        try:
            if self.conf.isDaemon == True: 
                if self.conf.mongo_shutdown == True:
                    self.conf.dockerManager.stopMongo()
                    self.printer.print_formatted_check("Shutdown Mongo Database", endingBreaks=1)  
                else:
                    self.printer.print_formatted_additional("Keeping Mongo Database Alive", endingBreaks=1)  

                # if self.conf.mongo_shutdown == True:
                #     # _docker_configer = NightcapDockerConfigurationHelper(self.conf)
                #     # _docker_configer.mongo_helper.continer_stop()
                #     self.conf.dockerManager.stop
                #     self.printer.print_formatted_check("Shutdown Mongo Server", endingBreaks=1)  
                # else:
                #     self.printer.print_formatted_additional("Keeping Ubuntu Alive", endingBreaks=1)  
            else:
                self.printer.print_formatted_check("Nothing To Shutdown", endingBreaks=1)  
                self.printer.print_formatted_check("Good Bye", endingBreaks=1)  
                
        except Exception as e:
            self.printer.print_error(e)
