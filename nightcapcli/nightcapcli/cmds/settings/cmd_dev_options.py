# region Imports
import traceback
from colorama import Fore, Style
from nightcapcore.invoker import Invoker
from nightcapcli.base.base_cmd import NightcapBaseCMD
from nightcapcore.lang_supported import PythonLangSupport, RubyLangSupport, GoLangSupport, RustLangSupport, PerlLangSupport
from nightcapcore.strategy.lang_strategy import LangStrategy
from nightcappackages.classes.commands import NightcapPackagePackerCommand
# endregion

class NightcapDevOptionsCMD(NightcapBaseCMD):
    """
    (User CLI Object)

    This class is used as a child class in the settings for developer options

    ...

    Attributes
    ----------
        ** Not including the ones from NightcapBaseCMD
            selectedList: -> list
                The current selected console path

    Methods
    -------
        Accessible
        -------
            help_genPackageUID(self): -> None
                Override for the genPackageUID commands help

            do_generate_package(self, package_path: str): -> None
                this will sign the package that the user passes into the program to be used later for installation

    """

    # region Init
    def __init__(self, selectedList: list, channelID: str = None) -> None:
        self.selectedList = selectedList
        NightcapBaseCMD.__init__(self, self.selectedList, channelid=channelID)
    # endregion

    # region Test Lang Support
    def do_testLangSupport(self, package_path: str) -> None:
        self.printer.print_underlined_header("Testing Python 3.8 Lang Support")
        _python = LangStrategy(PythonLangSupport(lang="python", version="3.8", lang_executor="python3.8"))
        _python.lang_info()
        _python.lang.test_lang()

        _python_pyenv = LangStrategy(PythonLangSupport(lang="python", version="3.9.0", lang_executor="python3.8"))

        if _python_pyenv.lang.check_support_by_platform():
            print("Language Version Exists")
        else:
            print("Language Version Needs Installed")
            if _python_pyenv.lang.install():
                if _python_pyenv.lang.check_support_by_platform():
                    print("Language Version Exists")
                else:
                    print("Language Version Needs Installed")
                

        self.printer.print_underlined_header("Testing Ruby Lang Support")
        _ruby = LangStrategy(RubyLangSupport(lang="ruby", version="2.7.0p0", lang_executor="ruby"))
        _ruby.lang_info()
        _ruby.lang.test_lang()

        self.printer.print_underlined_header("Testing Go Lang Support")
        _ruby = LangStrategy(GoLangSupport(lang="go", version="go1.18.1", lang_executor="go"))
        _ruby.lang_info()
        _ruby.lang.test_lang()

        self.printer.print_underlined_header("Testing Rust Lang Support")
        _ruby = LangStrategy(RustLangSupport(lang="rust", version="1.61.0", lang_executor="rustc"))
        _ruby.lang_info()
        _ruby.lang.test_lang()

        self.printer.print_underlined_header("Testing Perl Lang Support")
        _ruby = LangStrategy(PerlLangSupport(lang="perl", version="v5.30.0", lang_executor="perl"))
        _ruby.lang_info()
        _ruby.lang.test_lang()
        
        
    # endregion

    # region Do Generate Package
    def do_generate_package(self, package_path: str) -> None:
        try:
            invoker = Invoker()
            invoker.set_on_start(NightcapPackagePackerCommand(package_path))
            invoker.execute()
        except Exception as e:
            print(traceback.print_exc())
            raise e

    # endregion

    # region Help Generate Package
    def help_generate_package(self) -> None:
        h1 = "Generate UID for custom package:"
        h2 = "\tUsage ~ genPackageUID /path/to/package_info.json"
        p = """
         %s 
         %s
        """ % (
            (Fore.GREEN + h1),
            (Fore.YELLOW + h2 + Style.RESET_ALL),
        )
        print(p)
    # endregion
