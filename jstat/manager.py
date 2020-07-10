#!/usr/bin/env python
# coding: utf-8

import os
import logging
import pkgutil
import importlib
import pluggy

import jstat.spec

INSTALLED_DIR = os.path.dirname(jstat.spec.__file__)

log = logging.getLogger(__name__)

NAMESPACES = ('jstat.samplers', 'jstat.visualizers')

def get_manager():
    manager = pluggy.PluginManager("jstat")
    log.debug("get_manager() [start]")

    manager.add_hookspecs(jstat.spec)

    # modules in NAMESPACES (ie, internal modules) should automatically load
    for namespace in NAMESPACES:
        plugin_path = os.path.join(INSTALLED_DIR, *namespace.split('.')[1:])
        log.debug(f"loading {namespace}.* from {plugin_path}")
        for item in pkgutil.iter_modules([plugin_path], f"{namespace}."):
            if item.name == __name__:
                continue
            log.debug("loading %s", item.name)
            m = importlib.import_module(item.name)
            log.debug("loaded %s ==> %s, registering", item.name, m)
            manager.register(m)
            log.debug("registered %s", item.name)

    # modules outside of jstat itself (whether visualizers or samplers) should
    # load via entrypoints
    #
    # entry_points={
    #   "jstat_plugins": ['my_plugin_name = myproject.mymodule'],
    # }

    log.debug("loading setuptools 'jstat_plugins' entrypoints")
    manager.load_setuptools_entrypoints("jstat_plugins")

    log.debug("get_manager() [end]")

    return manager


Karen = get_manager
