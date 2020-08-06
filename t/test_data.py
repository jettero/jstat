#!/usr/bin/env python
# coding: utf-8


def test_flattened(twenty_item_sample_sets, twenty_flat_values):
    flat_ss_v = set(x.v for ss in twenty_item_sample_sets for x in ss.values())
    assert flat_ss_v == set(twenty_flat_values)


def test_dataset(twenty_item_data_set, twenty_tabled_values, five_names):
    headers, rows = twenty_item_data_set

    assert len(rows) == len(twenty_tabled_values)
    assert headers[1:] == five_names

    for ds_row, tv_row in zip(rows, twenty_tabled_values):
        assert tuple(ds_row[1:]) == tv_row
