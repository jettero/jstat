#!/usr/bin/env python3

from setuptools import setup

setup(
    name="jstat-plugin-example",
    author="Paul Miller",
    author_email="paul@jettero.pl",
    packages=["jpe"],
    entry_points={"jstat_plugins": ["jpe=jpe.blah"]}
)
