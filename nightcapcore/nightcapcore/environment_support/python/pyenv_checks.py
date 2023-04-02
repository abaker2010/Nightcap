import os
import re
import subprocess
from ..base import VirtualEnv_Checks

class PyenvChecks(VirtualEnv_Checks):
    def __init__(self) -> None:
        super().__init__()

    def clean_version(self, version: str) -> str:
        _version_regex = r"(?P<full_match>(\d+.\d+.\d+))|(?P<major_minor>(\d+.\d+))|(?P<major_only>(\d+))"
        _version_matches = re.match(_version_regex, version)
        _version_group_dict = _version_matches.groupdict()
        
        if _version_group_dict['full_match'] != None:
            return _version_group_dict['full_match']
        elif _version_group_dict['major_minor'] != None:
            return f"{_version_group_dict['major_minor']}.0"
        elif _version_group_dict['major_only'] != None:
            return f"{_version_group_dict['major_only']}.0.0"
        else:
            raise Exception("ERROR DETERMINING PYTHON VERSION TO USE :: NO MATCH")

    def check_env(self, env: str) -> bool:
        _envs_regex = r"\D+[^\d]"
        _envs = [x for x in os.listdir(os.path.join(os.environ.get('PYENV_ROOT'), "versions")) if re.match(_envs_regex, x) != None and x != ".DS_Store"]
        return True if env.strip() in _envs else False

    def check_version_downloadable(self, version: str) -> str:
        _versions = subprocess.run(
                [
                    "pyenv",
                    "install",
                    "-l"
                ],
                capture_output=True
            )

        _versions_cleaned = [x.strip() for x in _versions.stdout.decode("utf-8").split("\n")[1:-1]]
        return True if version in _versions_cleaned else False

    def check_version_installed(self, version: str) -> bool:
        _version_regex = r"\d+.\d+.\d+"
        if version.split('.')[-1] == '0':
            _versions = [x for x in os.listdir(os.path.join(os.environ.get('PYENV_ROOT'), "versions")) if re.match(_version_regex, x) != None]
        else:
            _versions = [x if x.split('.')[2] != '0' else '.'.join(x.split('.')[:2]) for x in os.listdir(os.path.join(os.environ.get('PYENV_ROOT'), "versions")) if re.match(_version_regex, x) != None]
        return True if version in _versions else False