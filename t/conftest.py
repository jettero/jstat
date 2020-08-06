# pylint: disable=redefined-outer-name
# coding: utf-8

import os
import sys
import subprocess
from glob import glob

import pytest
import jstat.manager


@pytest.fixture(scope="session")
def example_plugins():
    test_dir = os.path.dirname(__file__)
    src_dir = os.path.dirname(test_dir)
    example_dir = os.path.join(src_dir, "example-plugins")
    elib_dir = os.path.join(example_dir, "lib")

    sys.path.append(elib_dir)

    ret = list()

    base_cmd = ["pip", "install", "--target", elib_dir]
    for i in glob(os.path.join(example_dir, os.path.join("*", "setup.py"))):
        b = os.path.dirname(i)
        ret.append(os.path.basename(b))
        subprocess.check_call(base_cmd + [b])

    yield ret


@pytest.fixture(scope="session")
def jstat_mgr(example_plugins):  # pylint: disable=unused-argument
    yield jstat.manager.get_manager()
