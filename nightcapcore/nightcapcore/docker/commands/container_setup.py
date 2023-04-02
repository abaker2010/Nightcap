
# region Imports
from nightcapcore import Printer
from nightcapcore.command.command import Command
from nightcapcore.configuration.configuration import NightcapCLIConfiguration
# endregion

class NightcapDockerContainerSetup(Command):
    def __init__(self) -> None:
        super().__init__()
        self.printer = Printer()
        self.conf = NightcapCLIConfiguration()

    def execute(self) -> None:
        try:
            if self.conf.dockerClient.init_image(): 
                if self.conf.dockerClient.init_container():
                    self.conf.dockerClient.container_start()
                    self.printer.print_formatted_additional("Started Container", leadingTab=3)
                else:
                    self.printer.print_formatted_additional("Container Error", leadingTab=3)
                    raise Exception("Error with getting Mongo Init")
                return True
            else:
                raise Exception("Error with getting Mongo Image")
        except Exception as e:
            raise e