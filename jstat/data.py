# coding: utf-8

import time
from collections import OrderedDict, namedtuple

LOAD_TIME = time.time()


class Names(namedtuple("_Names", ["pkg", "name", "disp"])):
    """
    Container for information about where a value came from.
    :Names.pkg: The package that contains the ``name``
    :Names.name: The name of the class or function that produced this value
    :Names.short: The short or display name for the value (e.g., duration, size, etc)
    """

    def __new__(cls, pkg, name, disp=None, short=None):
        if name.startswith(pkg):
            name = name[len(pkg) + 1 :]

        if short is not None:
            disp = short

        if disp is None:
            disp = name

        return super().__new__(cls, pkg, name, disp)

    @property
    def long(self):
        return f"{self.pkg}.{self.name}"

    @long.setter
    def long(self, v):
        self.pkg, self.name = v.rsplit(".", maxsplit=1)

    @property
    def short(self):
        return f"{self.disp}"

    @short.setter
    def short(self, v):
        self.disp = v

    def __repr__(self):
        return f"<{self.name}:{self.disp}>"


class Sample:
    """
    Container for a sample, which has a time and a value.
    :Sample.t: time.time() by default
    :Sample.v: the actual value
    """

    def __init__(self, value, t=None):
        self.v = value
        self.t = time.time() if t is None else t

    @property
    def dt(self):
        return self.t - LOAD_TIME

    def __repr__(self):
        return f"{self.v}@{self.dt}"


def _check_key(k):
    if isinstance(k, (list, tuple)) and len(k) == 3:
        return Names(*k)
    if not isinstance(k, Names):
        raise ValueError("sample keys should always be jstat.sample.Names")
    return k


class SampleSet(OrderedDict):
    """ A set (presumably of all) the samples from a mainloop step """
    def __getitem__(self, k):
        k = _check_key(k)
        try:
            return super().__getitem__(k)
        except KeyError:
            pass

    def __setitem__(self, k, v):
        k = _check_key(k)
        if not isinstance(v, Sample):
            v = Sample(v)
        super().__setitem__(k, v)
