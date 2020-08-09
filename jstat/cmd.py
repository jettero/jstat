#!/usr/bin/env python
# coding: utf-8

import time
import click
import jstat.manager


@click.command()
def run():
    m = jstat.manager.get_manager()
    m.hook.get_samples()
    time.sleep(1)
    for i in m.hook.get_samples():
        for names, sample in i.items():
            header = m.hook.format_header(names=names)
            sample = m.hook.format_sample(sample=sample)

            if sample:
                print(f"{header}: {sample}")
