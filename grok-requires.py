#!/usr/bin/env python
# coding: utf-8

import distutils.core

setup = distutils.core.run_setup("setup.py")

todo = set()
for dsn in dir(setup):
    if dsn.startswith("_"):
        continue
    if dsn.endswith("_requires") or dsn.endswith("_require"):
        todo.add(dsn)

for ti in sorted(todo):
    attrval = getattr(setup, ti)
    if isinstance(attrval, (list, tuple)):
        print("#", ti)
        for avi in attrval:
            print(avi)
        print()
    elif isinstance(attrval, dict):
        for k, v in sorted(attrval.items()):
            print(f"# extras_require[{k}]")
            for _v in v:
                print(_v)
            print()
