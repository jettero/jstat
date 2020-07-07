#!/usr/bin/env python
# coding: utf-8

import pluggy

hookspec = pluggy.HookspecMarker('jstat')
hookimpl = pluggy.HookimplMarker('jstat')

@hookspec
def get_sample():
    pass
