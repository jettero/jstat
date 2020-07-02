# coding: utf-8

import time
from collections import OrderedDict, namedtuple

class Names( namedtuple('_Names', ['pkg', 'name', 'short']) ):
    """
    Container for information about where a value came from.
    :Names.pkg: The package that contains the ``name``
    :Names.name: The name of the class or function that produced this value
    :Names.short: The short or display name for the value (e.g., duration, size, etc)
    """

    @property
    def long(self):
        return '.'.join([ self.pkg, self.name ])

    @property
    def disp(self):
        return self.short

class Sample:
    """
    Container for a sample, which has a time and a value.
    :Sample.t: time.time() by default
    :Sample.v: the actual value
    """
    def __init__(self, value, t=None):
        self.v = value
        self.t = time.time() if t is None else t

class SampleSet(OrderedDict):
    def _check_key(self, k):
        if isinstance(k, (list,tuple)) and len(k) == 3:
            return Names(*k)
        if not isinstance(k, Names):
            raise ValueError("sample keys should always be jstat.Names")
        return k

    def __getitem__(self, k):
        k = self._check_key(k)
        try:
            return super().__getitem__(k)
        except KeyError:
            pass
        r = self[k] = list()
        return r

    def record(self, k, v, t=None):
        if not isinstance(v, Sample):
            v = Sample(v, t=t)
        elif t is not None:
            v = Sample(v.v, t=t)
        self[k].append(v)
