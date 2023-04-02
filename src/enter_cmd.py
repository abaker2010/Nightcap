from src.nightcap import Nightcap
from nightcapcore.command.command import Command
from nightcapcore.helpers.screen import ScreenHelper
from pymongo.errors import ServerSelectionTimeoutError

class EnterCMD(Command):
    def __init__(self) -> None:
        super().__init__()

    def execute(self) -> None:
        try:    
            ScreenHelper().clearScr()
            _who = Nightcap([], "basecli")

            l = _who.precmd("banner")
            r = _who.onecmd(l)
            r = _who.postcmd(r, l)
            if not r:
                _who.cmdloop()
        except ServerSelectionTimeoutError as e:
            raise Exception("Server time out :: %s" % str(e))
        except Exception as e:
            raise e