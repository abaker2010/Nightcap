
class Subscriber(object):
    """subscriber"""
    def __init__(self, name: str, broker, topic=None):
        self._name:str = name
        broker.attach(self)
        self.broker = broker
        self._topic = [] if topic is None else topic

    def sub(self, msg):
        print('[Subscriber: {}] got message: {}'.format(self._name, msg))

    def detach(self):
        self.broker.detach(self)

    @property
    def topic(self):
        return self._topic