from nightcapcli.observer.cli_broker import CLIBroker
from nightcapcore.singleton.singleton import Singleton
from nightcapcli.observer.bases.publisher import Publisher

class CLIPublisher(Publisher, metaclass=Singleton):
    def __init__(self):
        Publisher.__init__(self, "CLI-PUBLISHER", CLIBroker(), 'CLI_BROKER')