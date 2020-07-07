# pylint: disable=redefined-outer-name
# coding: utf-8

import pytest
import jstat.manager


@pytest.fixture(scope="session")
def manager():
    return jstat.manager.get_manager()


def test_plugins(manager):
    names = [x[0] for x in manager.list_name_plugin()]

    assert "jstat.plugins.proc_stat" in names
