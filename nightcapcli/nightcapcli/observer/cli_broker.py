from nightcapcli.observer.bases.broker import Broker
from nightcapcore.singleton.singleton import Singleton

class CLIBroker(Broker, metaclass=Singleton):
    def __init__(self):
        Broker.__init__(self,"CLI-BROKER")