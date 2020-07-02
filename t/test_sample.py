#!/usr/bin/env python
# coding: utf-8

import time
from jstat.sample import Names, SampleSet

def test_samples():
    t0 = time.time()
    v0 = 3.1415926
    l0 = ['pkg.name', 'ClassName', 'disp_name']
    n0 = Names(*l0)
    ss = SampleSet()
    ss.record(l0, v0)
    assert ss[l0][0].v == v0
    assert ss[l0][0].t >= t0
