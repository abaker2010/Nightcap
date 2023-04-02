from typing import Callable
from nightcapcore.printers import Printer
from nightcapcli.observer.bases.broker import Broker
from nightcapcli.observer.bases.subscriber import Subscriber
# from nightcapcore.configuration.configuration import NightcapCLIConfiguration

class CLISubscriber(Subscriber):
    def __init__(self, name: str, broker: Broker, callback: Callable[[str], bool] = None):
        super().__init__(name, broker, ['CLI_BROKER'])
        self.callback:Callable[[str], bool] = callback
        self.printer = Printer()

    def sub(self, msg:str):
        self.printer.debug(
                    '[Override :: Subscriber: {}] got message: {}'.format(self._name, msg),
                    # currentMode=NightcapCLIConfiguration().verbosity,
                )
        if self.callback != None:
            _called = self.callback(msg)
            if _called:
                self.printer.debug(
                    '[Callback (Message Successful) :: Subscriber: {}] :: ({})'.format(self._name, msg),
                    # currentMode=NightcapCLIConfiguration().verbosity,
                )
            else:
                self.printer.debug(
                    '[Callback (Message Failed) :: Subscriber: {}] :: ({})'.format(self._name, msg),
                    # currentMode=NightcapCLIConfiguration().verbosity,
                )