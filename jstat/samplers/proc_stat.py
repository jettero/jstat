#!/usr/bin/env python
# coding: utf-8

from jstat.spec import sampler_hookimpl
from jstat.data import SampleSet, Names

CPU_FIELDS = (
    "user",
    "nice",
    "system",
    "idle",
    "iowait",
    "irq",
    "softirq",
    "steal",
    "guest",
    "guest_nice",
)


@sampler_hookimpl
def get_samples():
    ret = SampleSet()
    with open("/proc/stat", "r") as fh:
        for line in fh:
            head, *values = line.strip().split()
            if head.startswith("cpu"):
                for n, v in zip(CPU_FIELDS, values):
                    name = Names(pkg=__package__, name=__name__, short=f"{head}.{n}")
                    ret[name] = v
    return ret
