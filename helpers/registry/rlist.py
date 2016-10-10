# -*- coding: utf-8 -*-
"""
helpers.registry.rlist

Helper functions to manage a registry list.

* created: 2013-06-18 Kevin Chan <kefin@makedostudio.com>
* updated: 2013-06-18 kchan
"""


def register(registry, params):
    """Add params to registry."""
    if isinstance(params, basestring):
        params = (params,)
    for s in params:
        if s and len(s) > 0:
            registry.append(s)


def unregister(registry, params):
    """Delete params from registry."""
    if isinstance(params, basestring):
        params = (params,)
    for s in params:
        if s in registry:
            registry.remove(s)


def is_registered(registry, name):
    """Lookup name in registry."""
    try:
        return name in registry
    except TypeError:
        pass
    return False
