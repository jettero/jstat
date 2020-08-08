# coding: utf-8

from jstat.spec import hookimpl
from jstat.util import seconds_to_interval


@hookimpl
def format_sample(sample):
    if sample.u == "s":
        return seconds_to_interval(sample.v)
