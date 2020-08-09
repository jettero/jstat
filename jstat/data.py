# coding: utf-8

import time
from collections import OrderedDict

LOAD_TIME = time.time()
UREG = None

try:
    import pint

    UREG = pint.UnitRegistry()
except:
    pass


class Names:
    """
    Container for information about where a value came from.
    :Names.pkg: The package that contains the ``name``
    :Names.name: The name of the class or function that produced this value
    :Names.disp: The short or display name for the value (e.g., duration, size, etc)
    """

    def __init__(self, pkg, name, disp=None, short=None):
        if name.startswith(f"{pkg}."):
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
        return not (self == other)

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
        return f"<{self.very_long}>"


class Sample:
    """
    Container for a sample, which has a time and a value.
    :Sample.t: time.time() by default
    :Sample.v: the actual value
    :Sample.u: the units as a string, if any
    :Sample.d: the time of some other thing

    Dynamic Properties
    :Sample.dt: gives the difference Sample.t - Sample.d
    :Sample.lt: gives the difference between LOAD_TIME and Sample.t
    """

    def __init__(self, v, u=None, t=None, d=None):
        self.v = v
        self.t = time.time() if t is None else t
        self.u = u
        self.d = d

    @property
    def dt(self):
        if self.d is None:
            return None
        return self.t - self.d

    @dt.setter
    def dt(self, v):
        self.d = v + self.t

    @property
    def lt(self):
        return self.t - LOAD_TIME

    @lt.setter
    def lt(self, v):
        self.t = LOAD_TIME + v

    def __repr__(self):
        return f"Sample({self.v}, u={self.u}, t={self.t:0.2f}, d={self.d:0.2f})"

    def __eq__(self, other):
        if isinstance(other, Sample):
            return other.v == self.v
        return self.v == other

    def __sub__(self, other):
        if isinstance(other, Sample):
            if self.u == other.u:
                return Sample(self.v - other.v, u=self.u, d=other.t)
            if self.u and other.u and UREG:
                sv = self.v * UREG[self.u]
                ov = other.v * UREG[other.u]
                return Sample((sv - ov).to(self.u).magnitude, u=self.u, d=other.t)
            raise TypeError(f"differing units ('{self.u}' vs '{other.u}')")
        return Sample(self.v - other, u=self.u)


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

    def __sub__(self, other):
        ret = self.__class__()
        if isinstance(other, SampleSet):
            for k in self:
                if k in other:
                    ret[k] = self[k] - other[k]
        else:
            for k in self:
                ret[k] = self[k] - other
        return ret


class DataTable:
    _time = Names(__package__, "time", "dt")

    def __init__(self, *sample_sets, previous=None):
        self._headers = previous.headers if previous else [self._time]
        self._rows = dict()
        for ss in sample_sets:
            self.add_sample_set(ss)

    def add_sample_set(self, sample_set):
        for name, sample in sample_set.items():
            t = int(sample.lt)
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
