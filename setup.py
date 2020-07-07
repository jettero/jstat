#!/usr/bin/env python3

import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

try:
    from sphinx.setup_command import BuildDoc
except ModuleNotFoundError:
    BuildDoc = None


class PyTest(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ""

    def run_tests(self):
        import shlex
        import pytest

        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


setup(
    name="jstat",
    description="Dstat clone in py3, with thoughts about pip-based plugins",
    author="Paul Miller",
    author_email="paul@jettero.pl",
    url="https://github.com/jettero/jstat",
    packages=find_packages(),
    cmdclass={"test": PyTest, "build_sphinx": BuildDoc},
    command_options={
        "build_sphinx": {
            "source_dir": ("setup.py", "doc/source"),
            "build_dir": ("setup.py", "doc/build"),
            "builder": ("setup.py", "html"),
            # because sphinx conf relies on reading jstat version
            # jstat must be installed to build the sphinx docs
            # (TODO: fix above somehow)
            #
            # To build html sphinx docs, ./setup.py --builder html
            # man with ./setup.py --builder man
        }
    },
    tests_require=["pytest"],
    install_requires=["pygments", "pluggy"],
    setup_requires=["setuptools_scm"],
    extras_require={"docs": ["sphinx"],},
    use_scm_version={
        "write_to": "jstat/__version__.py",
        "tag_regex": r"^(?P<prefix>v)?(?P<version>[^\+]+)(?P<suffix>.*)?$",
        # NOTE: use ./setup.py --version to regenerate version.py and print the
        # computed version
    },
    entry_points={"console_scripts": ["jstat = jstat.cmd:run"],},
)
