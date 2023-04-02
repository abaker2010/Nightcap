from typing import List
from nightcapcli.observer.bases.subscriber import Subscriber

class Broker(object):
    """
    Broker - Intermediate agent
    """
    def __init__(self, name: str, subscribers: List[str] = []):
        self._name = name
        self._subscribers = subscribers     # maintain a list of subscribers

    def attach(self, subscriber: Subscriber):
        """bind a subscriber"""
        if subscriber not in self._subscribers:
            self._subscribers.append(subscriber)

    def detach(self, subscriber: Subscriber):
        """unbind"""
        if subscriber in self._subscribers:
            self._subscribers.remove(subscriber)

    def route(self, msg, topic=''):
        """Methods of routing messages"""
        for subscriber in self._subscribers:
            if topic in subscriber.topic:
                subscriber.sub(msg)