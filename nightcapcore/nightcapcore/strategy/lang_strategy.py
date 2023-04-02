from nightcapcore.interface.ilangsupport import ILangSupport
from nightcapcore.interface.ilangstrategy import ILangStrategy
from typing import Dict
from os import system  

class LangStrategy(ILangStrategy):

    def __init__(self, lang: ILangSupport) -> None:
        super().__init__()
        self.lang = lang
    
    def exectue(self, *arg, **kwargs) -> Dict:
        return super().exectue(*arg, **kwargs)

    def information(self, *args, **kwargs) -> Dict:
        return super().information(*args, **kwargs)

    def lang_info(self):
        print("Lang:", self.lang.lang)
        print("Version:", self.lang.version)
        print("Executor:", self.lang.lang_executor)