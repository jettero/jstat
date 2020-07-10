#!/usr/bin/env python
# coding: utf-8

import pluggy

sampler_hookspec = pluggy.HookspecMarker("jstat")
sampler_hookimpl = pluggy.HookimplMarker("jstat")


@sampler_hookspec
def get_sample():
    pass
