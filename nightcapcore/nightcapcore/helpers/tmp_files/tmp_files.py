import shutil
import tempfile
from tempfile import TemporaryDirectory
from os.path import dirname, join, isdir
from os import mkdir, makedirs, sep, remove, rmdir
from typing import IO, List

# Developed from pypi documentation
# https://docs.python.org/3/library/tempfile.html
class NightcapTmpFiles():
    def __init__(self) -> None:
        self.tmp_file = None
        self.tmp_dir_context:TemporaryDirectory = None
        self.tmp_dir:str = None

    def create_folder(self) -> str:
        self.tmp_dir_context = tempfile.TemporaryDirectory()
        self.tmp_dir = self.tmp_dir_context.name
        return self.tmp_dir

    def create_file(self, mode='w+b', buffering=- 1, encoding=None, newline=None, suffix=None, prefix=None, dir=None, *, errors=None) -> IO[str] or IO[bytes]:
        self.tmp_file = tempfile.TemporaryFile(mode, buffering, encoding, newline, suffix, prefix, dir, errors)
        return self.tmp_file

    def clean_up(self):
        self.tmp_dir_context.cleanup()
