#!/usr/bin/env python3.8
# region Imports
import os
import sys
import colorama
import traceback
from time import sleep
from pymongo.errors import ServerSelectionTimeoutError
from nightcapcore.invoker import Invoker
from nightcapcore.printers.print import Printer
from nightcapcore.helpers.screen import ScreenHelper
from nightcapcore.banner.splash import Splash
from src.enter_cmd import EnterCMD
from src.boot_checks import NightcapBootChecks
from src.shutdown_checks import NightcapShutdownChecks

DEVNULL = open(os.devnull, "wb")
try:
    import readline

    if "libedit" in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")
except ImportError:
    sys.stdout.write("No readline module found, no tab completion available.\n")
else:
    import rlcompleter
# endregion


# region __NAME__
if __name__ == "__main__":
    try:
        colorama.init()

        Splash().getSplash()
        sleep(0.5)
        ScreenHelper().clearScr()
        
        _invoker = Invoker()
        _invoker.set_on_start(NightcapBootChecks())
        _invoker.execute()
        
        _invoker.set_on_start(EnterCMD())
        _invoker.execute()
        
    except KeyboardInterrupt as ke:
        ScreenHelper().clearScr()
        Printer().print_formatted_delete(text="Forced Termination!!", leadingBreaks=2, endingBreaks=1)
        exit()
    except ServerSelectionTimeoutError as e:
        Printer().print_error("ERROR CONNECTING WITH REMOTE CONTAINERS :: %s" % (str(e)))
    except Exception as e:
        traceback.print_exception()
        Printer().print_error(e)
    finally:
        Printer().print_underlined_header("Cleaning up...")
        try:
            _invoker = Invoker()
            _invoker.set_on_start(NightcapShutdownChecks())
            _invoker.execute()
        except Exception as e:
            Printer().print_error(e)

# endregion
