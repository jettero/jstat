#!/usr/bin/env python
# coding: utf-8

import pluggy
from jstat.data import SampleSet

sampler_hookspec = pluggy.HookspecMarker("jstat")
sampler_hookimpl = pluggy.HookimplMarker("jstat")

formatter_hookspec = pluggy.HookspecMarker("jstat")
formatter_hookimpl = pluggy.HookimplMarker("jstat")

visualizer_hookspec = pluggy.HookspecMarker("jstat")
visualizer_hookimpl = pluggy.HookimplMarker("jstat")

# Nothing actually runs these specs functions. They're given actions to
# demonstrate what you're meant to do with them.

@sampler_hookspec
def get_samples():
    # A SampleSet just a collection of samples, not ordered in a table.
    # Most plugins will produce more than one sample per loop. For example, the
    # proc_stat module reads all the things it can figure out from /proc/stat
    # and returns all those values as a SampleSet() for the timeslice.
    return SampleSet()

@formatter_hookspec
def format_samples(sample):
    # alter the appearance, scaling, units, etc
    return sample

@visualizer_hookspec
def visualize_samples(sample_set):
    headers, rows = sample_set.tableize()
    print(f'headers={headers}\nrows={rows}')

