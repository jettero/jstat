#!/usr/bin/env python
# coding: utf-8


def seconds_to_interval(x):
    conv = {"y": (365 * 86400), "d": 86400, "h": 3600, "m": 60}
    ret = ""
    for unit, uc in conv.items():
        v, x = divmod(x, uc)
        if v:
            ret += f"{v}{unit}"
    if x:
        ret += f"{x}s"
    return ret
