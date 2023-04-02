from abc import ABC, abstractmethod

class ILangSupport(ABC):
    """
    The Lang Support Interface is to allow for integration of new languages to the project
    
    """

    @abstractmethod
    def __init__(self, lang: str, version: str, lang_executor: str) -> None:
        super().__init__()
        self.lang = lang
        self.version = version
        self.lang_executor = lang_executor

    @abstractmethod
    def install(self):
        pass

    @abstractmethod
    def check_support_by_platform(self):
        pass

    @abstractmethod
    def test_lang(self):
        pass

