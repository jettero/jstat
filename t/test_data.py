#!/usr/bin/env python
# coding: utf-8

def test_twenty(twenty_item_sample_sets, twenty_flat_values):
    flat_ss_v = set( x.v for ss in twenty_item_sample_sets for x in ss.values() )
    assert flat_ss_v == set(twenty_flat_values)
