# -*- coding: utf-8 -*-
"""
helpers.registry.rdict

Helper functions to manage a registry dict.

* created: 2013-06-18 Kevin Chan <kefin@makedostudio.com>
* updated: 2013-06-18 kchan
"""


def register(registry, label, obj=None):
    registry[label] = obj

def unregister(registry, label):
    try:
        d = registry.get(label)
        del registry[label]
        return d
    except (AttributeError, KeyError, TypeError):
        return None

def is_registered(registry, label):
    """Lookup label in registry."""
    try:
        return label in registry
    except TypeError:
        pass
    return False

def get_object(registry, label, default_obj=None):
    return registry.get(label, default_obj)
