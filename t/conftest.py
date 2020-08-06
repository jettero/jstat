# pylint: disable=redefined-outer-name
# coding: utf-8

import os
import sys
import subprocess
from glob import glob

import pytest
import jstat.manager
from jstat.data import Names, Sample, SampleSet, DataTable, LOAD_TIME


@pytest.fixture
def twenty_tabled_values():
    yield (
        (1, 2, 3, 4, 5),
        (6, 7, 8, 9, 10),
        (11, 12, 13, 14, 15),
        (16, 17, 18, 19, 20),
    )


@pytest.fixture
def twenty_flat_values(twenty_tabled_values):
    ret = list()
    for row in twenty_tabled_values:
        ret.extend(row)
    yield ret


@pytest.fixture
def five_names():
    fn = zip(("one", "two", "three", "four", "five"), (0, 0, 2, 0, 3))
    yield [Names("tast", x, x[i]) for x, i in fn]


@pytest.fixture
def twenty_item_sample_sets(twenty_tabled_values, five_names):
    ret = list()
    for t, row in enumerate(twenty_tabled_values):
        ss = SampleSet()
        for name, value in zip(five_names, row):
            ss[name] = Sample(value, t=LOAD_TIME + t)
        ret.append(ss)
    yield ret


@pytest.fixture
def twenty_item_data_set(twenty_item_sample_sets):
    return DataTable(*twenty_item_sample_sets)


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
