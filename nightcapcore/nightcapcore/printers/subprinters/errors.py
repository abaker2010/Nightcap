
from nightcapcore.printers import PrinterBase
from colorama import Fore, Back, Style


class ErrorPrinter(PrinterBase):
    def __init__(self):
        super().__init__()

    def print_error(
        self,
        exception: Exception = None,
        message: object = None,
        *args,
        leadingText="[!]",
        errColor=Fore.RED,
        msgColor=Fore.LIGHTYELLOW_EX,
        optionalColor=Fore.YELLOW,
        leadingtab=1,
        vtab=1,
        endingBreaks=1,
        **kwargs
    ) -> None:
        self.base_print(
            str(exception),
            message,
            leadingColor=errColor,
            textColor=msgColor,
            optionalTextColor=optionalColor,
            leadingTab=leadingtab,
            vtabs=vtab,
            endingBreaks=endingBreaks,
            leadingText=leadingText,
            *args,
            **kwargs
        )
