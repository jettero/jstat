#!/usr/bin/env python
# coding: utf-8

import os
import sys
import logging
import pkgutil
import importlib
import pluggy

log = logging.getLogger(__name__)

def get_manager():
    manager = pluggy.PluginManager('jstat')
    log.debug('get_manager() [start]')

    # modules in jstat.plugins should automatically load if possible
    log.debug('loading jstat.plugins.*')
    import jstat.plugins
    plugin_path = os.path.dirname(jstat.plugins.__file__)
    manager.add_hookspecs(jstat.plugins)
    for item in pkgutil.iter_modules([plugin_path], "jstat.plugins."):
        if item.name == __name__:
            continue
        log.debug('loading %s', item.name)
        m = importlib.import_module(item.name)
        log.debug('loaded %s ==> %s, registering', item.name, m)
        manager.register(m)
        log.debug('registered %s', item.name)

    # other authors should do something like this in setup.py
    # entry_points={
    #   "jstat_plugins": ['my_plugin_name = myproject.mymodule'],
    # }
    log.debug('loading setuptools entrypoints')
    manager.load_setuptools_entrypoints('jstat_plugins')

    log.debug('get_manager() [end]')

    return manager

Karen = get_manager
