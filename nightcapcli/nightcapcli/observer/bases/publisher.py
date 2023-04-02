from nightcapcore.printers import Printer
from nightcapcli.observer.bases.broker import Broker

class Publisher(object):
    """announcer"""
    def __init__(self, name: str, broker: Broker, topic: str):
        self._name:str = name
        self._broker:Broker = broker
        self._topic:str = topic
        self.printer = Printer()

    def pub(self, msg):
        self.printer.debug(
                    '[Publisher: {}] topic: {}, message: {}'.format(self._name, self._topic, msg),
                )
        self._broker.route(msg, self._topic)
