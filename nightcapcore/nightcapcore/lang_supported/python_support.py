from nightcapcore.interface.ilangsupport import ILangSupport
from os import system
import subprocess


class PythonLangSupport(ILangSupport):
    
    def __init__(self, lang: str, version: str, lang_executor: str) -> None:
        super().__init__(lang, version, lang_executor)

    def install(self):
        print("Installing Version: %s" % self.version)
        proc = subprocess.Popen([("pyenv install %s" % self.version)], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        print(out)
        print("Install Done")
        return True

    def check_support_by_platform(self) -> bool:
        print("Checking to see if the version exsits")
        proc = subprocess.Popen(["pyenv versions"], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        _split = str(out.decode()).split('\n')
        print(_split)
        print("Looking for : %s" % self.version)
        for ver in _split:
            print(ver)
            if self.version in ver:
                return True

            return False


    
    def test_lang(self):
        print("Testing")
        _test = ("%s --version" % self.lang_executor)
        system(_test)
        print("Done Testing")