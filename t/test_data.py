#!/usr/bin/env python
# coding: utf-8

from jstat.data import Names, SampleSet


def test_flattened(twenty_item_sample_sets, twenty_flat_values):
    flat_ss_v = set(x.v for ss in twenty_item_sample_sets for x in ss.values())
    assert flat_ss_v == set(twenty_flat_values)


def test_dataset(twenty_item_data_set, twenty_tabled_values, five_names):
    headers, rows = twenty_item_data_set

    assert len(rows) == len(twenty_tabled_values)
    assert headers[1:] == five_names

    for ds_row, tv_row in zip(rows, twenty_tabled_values):
        assert tuple(ds_row[1:]) == tv_row


def test_names_keys():
    ss = SampleSet()
    assert len(ss) == 0

    n1 = Names("p1", "namehere", "nh")
    n2 = Names("p1", "namehere", "nh")
    n3 = Names("p2", "namehere", "nh")

    ss[n1] = 7
    ss[n2] = 8
    ss[n3] = 9

    assert len(ss) == 2
    assert ss[n1] == 8
    assert ss[n2] == 8
    assert ss[n3] == 9

    assert ss["namehere"] == 9
    assert ss["nh"] == 9
    assert ss["p2.namehere"] == 9
