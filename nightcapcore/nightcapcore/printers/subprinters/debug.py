
from nightcapcore.configuration.configuration import NightcapCLIConfiguration
from nightcapcore.printers.base import PrinterBase
from colorama import Fore

class DebugPrinter(PrinterBase):
    def __init__(self):
        self.currentMode = NightcapCLIConfiguration().verbosity
        super(PrinterBase, self).__init__()

    def debug(
        self,
        text: object = None,
        optionaltext: object = None,
        # currentMode: bool = False,
        *args,
        leadingText="[DEBUG]",
        leadingTab=0,
        optionalTextColor=Fore.LIGHTBLACK_EX,
        textColor=Fore.LIGHTCYAN_EX,
        leadingColor=Fore.MAGENTA,
        **kwargs
    ) -> None:
        # print("Text", text)
        # print("Optional",optionaltext)
        if self.currentMode == True:
            self.base_print(
                text,
                optionaltext,
                *args,
                leadingText=leadingText,
                leadingTab=leadingTab,
                leadingColor=leadingColor,
                textColor=textColor,
                optionalTextColor=optionalTextColor,
                **kwargs
            )
        # self.base_print(self,text, optionaltext)

    def debug_add_to_list(
        self,
        text: object = None,
        optionaltext: object = None,
        # currentMode: bool = False,
        *args,
        leadingText="[DEBUG]",
        leadingTab=0,
        optionalTextColor=Fore.LIGHTBLACK_EX,
        textColor=Fore.LIGHTCYAN_EX,
        leadingColor=Fore.MAGENTA,
        **kwargs
    ) -> str:
        # print("Text", text)
        # print("Optional",optionaltext)
        if self.currentMode == True:
            return self.base_print(
                text,
                optionaltext,
                *args,
                leadingText=leadingText,
                leadingTab=leadingTab,
                leadingColor=leadingColor,
                textColor=textColor,
                optionalTextColor=optionalTextColor,
                **kwargs
            )
        # self.base_print(self,text, optionaltext)
