#!/usr/bin/env python
# coding: utf-8

import click
import jstat.manager


@click.command()
def run():
    m = jstat.manager.get_manager()
    for i in m.hook.get_samples():
        print(f"i={i}")
