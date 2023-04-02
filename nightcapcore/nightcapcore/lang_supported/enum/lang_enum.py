from enum import Enum

class NoValue(Enum):
     def __repr__(self):
         return '<%s.%s>' % (self.__class__.__name__, self.name)


class LangEnum(Enum):
    GO = "go",
    PERL = "perl",
    PYTHON = "python",
    RUBY = "ruby",
    RUST = "rust"

    def __str__(self) -> str:
        return self.value[0]

    # @classmethod
    # def from_string(cls, s):
    #     for lang in cls:
    #         print("Lang :: %s" % lang)
    #         if lang.value == s:
    #                 return lang
    #     raise ValueError(cls.__name__ + ' has no value matching "' + s + '"')
