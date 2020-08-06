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

NAMESPACES = ("jstat.samplers", "jstat.visualizers")


class JstatManager(pluggy.PluginManager):
    _local_modules = set()

    @property
    def local_modules(self):
        yield from self._local_modules if self._local_modules else self._load_local_modules()

    @classmethod
    def _load_local_modules(cls):
        """
        load modules that are part of the jstat package modules outside jstat
        should provide an entry point which will get picked up during the
        JstatManager initialization.

        I.e., in your setup.py, provide something like this:

            entry_points={
              "jstat_plugins": ['my_plugin_name = myproject.mymodule'],
            }

        jstat will load the plugins via pluggy

            class JstatManager(pluggy.PluginManager):
                def __init__(self):
                    ... snip ...
                    self.load_setuptools_entrypoints("jstat_plugins")
                    ... snip ...
        """

        if cls._local_modules:
            return cls._local_modules

        for namespace in NAMESPACES:
            plugin_path = os.path.join(INSTALLED_DIR, *namespace.split(".")[1:])
            log.debug("loading %s.* from %s", namespace, plugin_path)
            for item in pkgutil.iter_modules([plugin_path], f"{namespace}."):
                if item.name == __name__:
                    continue
                log.debug("loading %s", item.name)
                m = importlib.import_module(item.name)
                cls._local_modules.add(m)

        return cls._local_modules

    def __init__(self):
        super().__init__("jstat")

        log.debug("JstatManager.init [start]")

        self.add_hookspecs(jstat.spec)
        for m in self.local_modules:
            log.debug("registering %m", m)
            self.register(m)
            log.debug("registered %s", m)

        log.debug("loading setuptools 'jstat_plugins' entrypoints")
        self.load_setuptools_entrypoints("jstat_plugins")

        log.debug("JstatManager.init [end]")


_manager = None


def get_manager():
    global _manager
    if _manager is None:
        _manager = JstatManager()
    return _manager


Karen = get_manager
