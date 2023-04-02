
# from application.classes.helpers.printers.base.printer_base import PrinterBase
from nightcapcore.printers import PrinterBase
from colorama import Fore, Back, Style


class CheckMarkPrinter(PrinterBase):
    def __init__(self):
        super().__init__()

    def print_formatted_other(
        self,
        text,
        optionaltext=None,
        *args,
        leadingText="[*]",
        leadingBreaks=0,
        endingBreaks=0,
        vtabs=0,
        leadingTab=1,
        leadingColor=Fore.LIGHTGREEN_EX,
        textColor=Fore.LIGHTGREEN_EX,
        optionalTextColor=Fore.LIGHTBLACK_EX,
        breakTextColor=Fore.LIGHTBLACK_EX,
        **kwargs
    ) -> None:
        self.base_print(
            text,
            optionaltext,
            leadingText=leadingText,
            leadingTab=leadingTab,
            leadingBreaks=leadingBreaks,
            endingBreaks=endingBreaks,
            vtabs=vtabs,
            leadingColor=leadingColor,
            optionalTextColor=optionalTextColor,
            textColor=textColor,
            breakTextColor=breakTextColor,
            *args,
            **kwargs
        )

    def print_formatted_check(
        self,
        text,
        optionaltext=None,
        *args,
        leadingBreaks=0,
        endingBreaks=0,
        vtabs=0,
        leadingTab=2,
        leadingText="[✓]",
        leadingColor=Fore.LIGHTGREEN_EX,
        textColor=Fore.LIGHTGREEN_EX,
        optionalTextColor=Fore.LIGHTBLACK_EX,
        breakTextColor=Fore.LIGHTBLACK_EX,
        **kwargs
    ) -> None:
        self.base_print(
            text,
            optionaltext,
            leadingText=leadingText,
            leadingTab=leadingTab,
            leadingBreaks=leadingBreaks,
            endingBreaks=endingBreaks,
            vtabs=vtabs,
            leadingColor=leadingColor,
            optionalTextColor=optionalTextColor,
            textColor=textColor,
            breakTextColor=breakTextColor,
            *args,
            **kwargs
        )

    def print_formatted_additional(
        self,
        text,
        optionaltext=None,
        *args,
        leadingBreaks=0,
        endingBreaks=0,
        vtabs=0,
        leadingTab=2,
        leadingColor=Fore.YELLOW,
        textColor=Fore.LIGHTGREEN_EX,
        optionalTextColor=Fore.LIGHTBLACK_EX,
        breakTextColor=Fore.LIGHTBLACK_EX,
        **kwargs
    ) -> None:
        self.base_print(
            text,
            optionaltext,
            leadingText="[>]",
            leadingTab=leadingTab,
            leadingBreaks=leadingBreaks,
            endingBreaks=endingBreaks,
            vtabs=vtabs,
            leadingColor=leadingColor,
            optionalTextColor=optionalTextColor,
            textColor=textColor,
            breakTextColor=breakTextColor,
            *args,
            **kwargs
        )

    def print_formatted_delete(
        self,
        text,
        optionaltext=None,
        *args,
        leadingBreaks=0,
        endingBreaks=0,
        vtabs=0,
        leadingTab=2,
        leadingColor=Fore.RED,
        textColor=Fore.LIGHTYELLOW_EX,
        optionalTextColor=Fore.LIGHTBLACK_EX,
        breakTextColor=Fore.LIGHTBLACK_EX,
        **kwargs
    ) -> None:
        self.base_print(
            text,
            optionaltext,
            leadingText="[x]",
            leadingTab=leadingTab,
            leadingBreaks=leadingBreaks,
            endingBreaks=endingBreaks,
            vtabs=vtabs,
            leadingColor=leadingColor,
            optionalTextColor=optionalTextColor,
            textColor=textColor,
            breakTextColor=breakTextColor,
            *args,
            **kwargs
        )
