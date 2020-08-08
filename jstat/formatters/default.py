# coding: utf-8

from jstat.spec import hookimpl


@hookimpl(trylast=True)
def format_header(names):
    return names.disp


@hookimpl(trylast=True)
def format_sample(sample):
    return sample.v
