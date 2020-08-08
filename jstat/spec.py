#!/usr/bin/env python
# coding: utf-8

import pluggy
from jstat.data import SampleSet

hookspec = pluggy.HookspecMarker("jstat")
hookimpl = pluggy.HookimplMarker("jstat")

# Nothing actually runs these specs functions. They're given actions to
# demonstrate what you're meant to do with them.


@hookspec
def get_samples():
    # A SampleSet just a collection of samples, not ordered in a table.
    # Most plugins will produce more than one sample per loop. For example, the
    # proc_stat module reads all the things it can figure out from /proc/stat
    # and returns all those values as a SampleSet() for the timeslice.
    return SampleSet()


@hookspec(firstresult=True)
def format_header(names):
    # choose one of the names
    return names.disp


@hookspec(firstresult=True)
def format_sample(sample):
    # reformat seconds into hours or adjust the shown precision
    return sample.v


@hookspec
def visualize_samples(sample_set):
    headers, rows = sample_set.tableize()
    print(f"headers={headers}\nrows={rows}")


del hookspec
