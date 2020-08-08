# coding: utf-8

import os

from jstat.spec import hookimpl
from jstat.data import SampleSet, Names, Sample

SC_CLK_TCK = os.sysconf("SC_CLK_TCK")

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


def _time_decode(x):
    return int(int(x) / SC_CLK_TCK)


@hookimpl
def get_samples():
    ret = SampleSet()
    with open("/proc/stat", "r") as fh:
        for line in fh:
            head, *values = line.strip().split()
            if head.startswith("cpu"):
                for n, v in zip(CPU_FIELDS, values):
                    name = Names(pkg=__package__, name=f"{head}.{n}")
                    ret[name] = Sample(_time_decode(v), units="s")
            if head.startswith("intr"):
                for i, v in enumerate(values):
                    v = int(v)
                    if v > 0:
                        name = "irq.total" if i == 0 else f"irq{i}"
                        ret[Names(pkg=__package__, name=name)] = Sample(v)
    return ret
