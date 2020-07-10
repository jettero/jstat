#!/usr/bin/env python
# coding: utf-8

import time
from jstat.data import Names, SampleSet

def test_samples():
    t0 = time.time()
    v0 = 3.1415926
    l0 = ["pkg.name", "ClassName", "disp_name"]
    n0 = Names(*l0)
    ss = SampleSet()
    ss[l0] = v0

    assert ss[l0].v == v0
    assert ss[l0].t >= t0

    assert ss[n0].v == v0
    assert ss[n0].t >= t0

    for k in ss:
        assert isinstance(k, Names)
