from __future__ import with_statement

import os
import re

import setuptools

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


NAME = "nightcappackages"


def read_file(path):
    with open(os.path.join(os.path.dirname(__file__), path)) as fp:
        return fp.read()


def _get_version_match(content):
    # Search for lines of the form: # __version__ = 'ver'
    regex = r"^__version__ = ['\"]([^'\"]*)['\"]"
    version_match = re.search(regex, content, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def get_version(path):
    return _get_version_match(read_file(path))


setup(
    name=NAME,
    version=get_version(os.path.join("nightcappackages", "__init__.py")),
    description="Default Package library for Nightcap",
    url="https://github.com/abaker2010/nightcap",
    author="Aaron Baker",
    author_email="crosby.baker@gmail.com",
    license="BSD 3-Clause",
    packages=setuptools.find_packages(),
    install_requires=[NAME],
    classifiers=[

        "Programming Language :: Python :: 3",

        "Operating System :: OS Independent",

    ],
    python_requires='>=3.8.1',
)
