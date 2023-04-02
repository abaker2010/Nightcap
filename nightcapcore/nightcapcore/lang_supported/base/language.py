from __future__ import annotations
from abc import ABC


class LanguageSupported(ABC):
    def __init__(self, lang: str, version: str, enabled: bool) -> None:
        super().__init__()
        self.language = lang
        self.version = version
        self.enabled = enabled
        
    def from_json(jsonData: dict) -> LanguageSupported:
        return LanguageSupported(**jsonData)

    def __str__(self) -> str:
        return f'{self.language} : {self.version}'