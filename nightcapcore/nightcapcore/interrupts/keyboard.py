import signal
from nightcapcore.singleton.singleton import Singleton
from nightcapcore import Printer

class KeyboardInterruptHandler(metaclass=Singleton):
    def __init__(self) -> None:
        self.interrupt_count = 0
        self.printer = Printer()

    def reset_count(self):
        self.interrupt_count = 0

    def interrupt(self) -> bool:
        if self.interrupt_count == 0:
            self.interrupt_count += 1
            return False
        elif self.interrupt_count == 1:
            return True
        else:
            pass
