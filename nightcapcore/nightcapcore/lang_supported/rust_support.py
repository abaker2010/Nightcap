from nightcapcore.interface.ilangsupport import ILangSupport
from os import system

class RustLangSupport(ILangSupport):
    def __init__(self, lang: str, version: str, lang_executor: str) -> None:
        super().__init__(lang, version, lang_executor)

    def install(self):
        return super().install()

    def check_support_by_platform(self):
        return super().check_support_by_platform()
    
    def test_lang(self):
        print("Testing")
        _test = ("%s --version" % self.lang_executor)
        system(_test)
        print("Done Testing")