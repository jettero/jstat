#!/usr/bin/env python
# coding: utf-8

from jstat.spec import sampler_hookimpl
from jstat.data import SampleSet, Names

DATA = dict(blah=0)


@sampler_hookimpl
def blah():
    ret = SampleSet()
    name = Names(pkg=__package__, name=__name__, short="jpe")
    ret[name] = f"data{DATA['blah']}"
    DATA["blah"] += 1
    return ret
