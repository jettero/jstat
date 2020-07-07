#!/usr/bin/env python
# coding: utf-8

import jstat.plugins as jp

CPU_FIELDS = ('user', 'nice', 'system', 'idle', 'iowait', 'irq', 'softirq', 'steal', 'guest', 'guest_nice')

@jp.hookimpl
def get_samples(test12):
    ret = SampleSet()
    with open('/proc/stat', 'r') as fh:
        for line in fh:
            head,*values = line.strip().split()
            if head.startswith('cpu'):
                for n,v in zip(CPU_FIELDS, values):
                    name = Names(pkg=__package__, name=__name__, short=f'{head}.{n}')
                    ret[name] = v
    return ret
