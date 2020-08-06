# coding: utf-8


def test_plugins(jstat_mgr, example_plugins):
    names = [x[0] for x in jstat_mgr.list_name_plugin()]

    assert "jstat.samplers.proc_stat" in names
    assert len(example_plugins) > 0
    for item in example_plugins:
        assert item in names
