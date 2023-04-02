
from nightcapcore.printers import PrinterBase
from colorama import Fore, Back, Style


class ItemPrinter(PrinterBase):
    def __init__(self):
        super().__init__()

    def item_1(
        self,
        text="",
        optionalText=None,
        *args,
        leadingTab=2,
        leadingText="[-]",
        leadingBreaks=0,
        endingBreaks=0,
        vtabs=0,
        seperator=" -> ",
        leadingColor=Fore.LIGHTGREEN_EX,
        textColor=Fore.LIGHTYELLOW_EX,
        optionalTextColor=Fore.LIGHTBLUE_EX,
        breakTextColor=Fore.LIGHTMAGENTA_EX,
        styleRest=Style.RESET_ALL,
        **kwargs
    ) -> None:

        self.base_print(
            text,
            optionalText,
            leadingText=leadingText,
            leadingTab=leadingTab,
            leadingBreaks=leadingBreaks,
            endingBreaks=endingBreaks,
            vtabs=vtabs,
            leadingColor=leadingColor,
            textColor=textColor,
            optionalTextColor=optionalTextColor,
            seperator=seperator,
            breakTextColor=breakTextColor,
            styleRest=styleRest,
            *args,
            **kwargs
        )

    def item_2(
        self,
        text="",
        optionalText=None,
        *args,
        leadingTab=3,
        leadingText="-",
        leadingBreaks=0,
        endingBreaks=0,
        vtabs=0,
        seperator=" : ",
        leadingColor=Fore.LIGHTGREEN_EX,
        textColor=Fore.LIGHTYELLOW_EX,
        optionalTextColor=Fore.LIGHTBLUE_EX,
        breakTextColor=Fore.LIGHTMAGENTA_EX,
        styleRest=Style.RESET_ALL,
        **kwargs
    ) -> None:
        self.base_print(
            text,
            optionalText,
            leadingText=leadingText,
            leadingTab=leadingTab,
            leadingBreaks=leadingBreaks,
            endingBreaks=endingBreaks,
            vtabs=vtabs,
            leadingColor=leadingColor,
            textColor=textColor,
            optionalTextColor=optionalTextColor,
            seperator=seperator,
            breakTextColor=breakTextColor,
            styleRest=styleRest,
            *args,
            **kwargs
        )

    def item_3(
        self,
        text="",
        optionalText=None,
        *args,
        leadingTab=4,
        leadingText="*",
        leadingBreaks=0,
        endingBreaks=0,
        vtabs=0,
        seperator=" : ",
        leadingColor=Fore.LIGHTGREEN_EX,
        textColor=Fore.LIGHTYELLOW_EX,
        optionalTextColor=Fore.LIGHTBLUE_EX,
        breakTextColor=Fore.LIGHTMAGENTA_EX,
        styleRest=Style.RESET_ALL,
        **kwargs
    ) -> None:

        self.base_print(
            text,
            optionalText,
            leadingText=leadingText,
            leadingTab=leadingTab,
            leadingBreaks=leadingBreaks,
            endingBreaks=endingBreaks,
            vtabs=vtabs,
            leadingColor=leadingColor,
            textColor=textColor,
            optionalTextColor=optionalTextColor,
            seperator=seperator,
            breakTextColor=breakTextColor,
            styleRest=styleRest,
            *args,
            **kwargs
        )

    def help(
        self,
        text="",
        optionalText=None,
        *args,
        leadingTab=1,
        leadingText="~",
        leadingBreaks=0,
        endingBreaks=1,
        vtabs=1,
        seperator=" : ",
        leadingColor=Fore.LIGHTGREEN_EX,
        textColor=Fore.LIGHTGREEN_EX,
        optionalTextColor=Fore.LIGHTBLUE_EX,
        breakTextColor=Fore.LIGHTMAGENTA_EX,
        styleRest=Style.RESET_ALL,
        **kwargs
    ) -> None:

        self.base_print(
            text,
            optionalText,
            leadingText=leadingText,
            leadingTab=leadingTab,
            leadingBreaks=leadingBreaks,
            endingBreaks=endingBreaks,
            vtabs=vtabs,
            leadingColor=leadingColor,
            textColor=textColor,
            optionalTextColor=optionalTextColor,
            seperator=seperator,
            breakTextColor=breakTextColor,
            styleRest=styleRest,
            *args,
            **kwargs
        )
