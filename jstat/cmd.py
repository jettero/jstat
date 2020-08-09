#!/usr/bin/env python
# coding: utf-8

import time
import click
import tabulate

import jstat.manager
from jstat.data import DataTable


@click.command()
@click.option("--filter", "-f", type=str, multiple=True)
def run(filter):
    m = jstat.manager.get_manager()
    m.hook.get_samples()
    dt = DataTable(
        filter=filter,
        format_header=m.hook.format_header,
        format_sample=m.hook.format_sample,
    )
    while True:
        time.sleep(1)
        for ss in m.hook.get_samples():
            dt.add_sample_set(ss)
        t = tabulate.tabulate(dt.rows, headers=dt.headers)
        for i in range(100):
            print()
        print(t)
