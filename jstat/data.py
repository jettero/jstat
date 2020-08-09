# coding: utf-8

import time
from collections import OrderedDict, namedtuple

LOAD_TIME = time.time()


class Names:
    """
    Container for information about where a value came from.
    :Names.pkg: The package that contains the ``name``
    :Names.name: The name of the class or function that produced this value
    :Names.disp: The short or display name for the value (e.g., duration, size, etc)
    """

    def __init__(self, pkg, name, disp=None, short=None):
        if name.startswith(f'{pkg}.'):
            name = name[len(pkg) + 1 :]

        if short is not None:
            disp = short

        if disp is None:
            disp = name

        self.pkg = pkg
        self.name = name
        self.disp = disp


    def __hash__(self):
        return hash(self.very_long)

    def __eq__(self, other):
        return isinstance(other, Names) and self.very_long == other.very_long

    def __ne__(self, other):
        return not(self == other)

    @property
    def very_long(self):
        if self.disp and self.disp != self.name:
            return f"{self.pkg}.{self.name}:{self.disp}"
        return f"{self.pkg}.{self.name}"

    @property
    def long(self):
        return f"{self.pkg}.{self.name}"

    @long.setter
    def long(self, v):
        self.pkg, self.name = v.rsplit(".", maxsplit=1)

    @property
    def short(self):
        return self.disp

    @short.setter
    def short(self, v):
        self.disp = v

    def __repr__(self):
        return f'<{self.very_long}>'


class Sample:
    """
    Container for a sample, which has a time and a value.
    :Sample.t: time.time() by default
    :Sample.v: the actual value
    """

    def __init__(self, value, units=None, t=None):
        self.v = value
        self.t = time.time() if t is None else t
        self.u = units

    @property
    def dt(self):
        return self.t - LOAD_TIME

    def __repr__(self):
        if self.u:
            return f"{self.v}{self.u}@{self.dt}"
        return f"{self.v}@{self.dt}"

    def __eq__(self, other):
        if isinstance(other, Sample):
            return other.v == self.v
        return self.v == other


class SampleSet(OrderedDict):
    """
    A set (presumably of all) the samples from a mainloop step.  Really just an
    ordered dict mapping names to sample values.

    It is *not* a table of historical data.
    """

    def _check_key(self, k):
        o = k
        if isinstance(k, str):
            for i in reversed(self):
                if k in (i.name, i.disp, i.short, i.long):
                    return i
            k = k.split(".")
        if isinstance(k, (list, tuple)) and len(k) in (2, 3):
            return Names(*k)
        if not isinstance(k, Names):
            raise ValueError(f"unable to resolve '{o}' into jstat.sample.Names")
        return k

    def tableize(self, previous=None):
        return DataTable(self, previous=previous)

    def __getitem__(self, k):
        k = self._check_key(k)
        try:
            return super().__getitem__(k)
        except KeyError:
            pass

    def __setitem__(self, k, v):
        k = self._check_key(k)
        if not isinstance(v, Sample):
            v = Sample(v)
        super().__setitem__(k, v)


class DataTable:
    _time = Names(__package__, "time", "dt")

    def __init__(self, *sample_sets, previous=None):
        self._headers = previous.headers if previous else [self._time]
        self._rows = dict()
        for ss in sample_sets:
            self.add_sample_set(ss)

    def add_sample_set(self, sample_set):
        for name, sample in sample_set.items():
            t = int(sample.dt)
            if t not in self._rows:
                self._rows[t] = d = dict()
                d[self._time] = t
            self._rows[t][name] = sample.v
            if name not in self._headers:
                self._headers.append(name)

    @property
    def headers(self):
        return self._headers

    @property
    def row_iter(self):
        for t in sorted(self._rows):
            yield [self._rows[t].get(name, None) for name in self.headers]

    @property
    def rows(self):
        return list(self.row_iter)

    def __iter__(self):
        yield from (self.headers, self.rows)
