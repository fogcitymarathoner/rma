# -*- coding: utf-8 -*-
"""
minipylib.utils

Utility functions.

Copyright (c) 2011-2012 Kevin Chan <kefin@makedostudio.com>

* created: 2011-04-17 Kevin Chan <kefin@makedostudio.com>
* updated: 2012-06-25 kchan
"""

import sys
import os
import imp
import hashlib
import codecs
import itertools
import logging



### add directory to module search path (sys.path)

def add_to_sys_path(path):
    """
    Add directory to ``sys.path``.

    :param path: module directory to add to ``sys.path``.
    """
    if os.path.isdir(path):
        sys.path.append(path)


### import module given path

def import_module(path):
    """
    Dynamically import module from path and return a module object.

    :param path: file path of module to import.
    :returns: module or `None` if error.
    """
    try:
        assert path is not None and os.path.isfile(path)
        src = open(path, 'rb')
        m = hashlib.sha1()
        m.update(path)
        module = imp.load_source(m.hexdigest(), path, src)
        src.close()
    except (TypeError, AssertionError, IOError):
        module = None
    return module


### import vars from modules

def import_module_vars(module, *args):
    """
    Import vars from module.

    :param module: module name.
    :param args: list of variables to import.
    :returns: None on error, otherwise `dict` of name/values. If no `args`,
        return module `__dict__`.

    Example::

        data = import_module_vars('webapp.urls', 'URLS')

    :More info: `<http://stackoverflow.com/questions/2259427/load-python-code-at-runtime>`_

    """
    try:
        m = __import__(module, globals(), locals(), args, -1)
    except ImportError:
        return None

    if module.find('.') != -1:
        # submodule
        m = sys.modules[module]

    if len(args) == 0:
        result = m.__dict__
    else:
        result = {}
        for name in args:
            try:
                result[name] = getattr(m, name)
            except AttributeError:
                result[name] = None
    return result


def import_module_settings(module):
    """
    Import settings from module.

    * only global vars in ALL CAPS are imported.

    :param module: name of module to import from.
    :returns: imported settings or `None` on error.
    """
    data = import_module_vars(module)
    try:
        settings = dict([(k, v) for k, v in data.items() if k == k.upper()])
    except AttributeError:
        return None
    return settings


### create class instance based on module and class name

def get_instance(module, class_name, *args, **kwargs):
    """
    Return an instance of the object based on module name and class name.

    :param module: module name.
    :param class_name: name of class to instantiate.
    :param args: args to pass to class.
    :param kwargs: keyword args to pass to class.
    :returns: instance of class.
    """
    __import__(module)
    f = getattr(sys.modules[module], class_name)
    return f(*args, **kwargs)


### get text file content

default_encoding = "utf-8"

def get_file_contents(path, encoding=default_encoding):
    """
    Load text file from file system and return content as string.

    :param path: path of file to read.
    :param encoding: file encoding (default is `utf-8`).
    :returns: file content as string or `None` if file cannot be read.
    """
    try:
        assert path is not None and os.path.isfile(path)
        file_obj = codecs.open(path, "r", encoding)
        data = file_obj.read()
        file_obj.close()
    except (TypeError, AssertionError, IOError):
        data = None
    return data


def write_file(path, data, encoding=default_encoding):
    """
    Write text file to file system.

    :param path: path of file to write to.
    :param data: data to write.
    :param encoding: data encoding (default is `utf-8`, set to None for no encoding)
    :returns: `True` if no error or `False` if ``IOError``.
    """
    try:
        the_file = open(path, 'wb')
        if encoding:
            data = data.encode(encoding)
        the_file.write(data)
        the_file.close()
        return True
    except IOError:
        return False


def delete_file(path):
    """
    Truncates file to zero size and
    tries to unlink file if possible.

    :param path: file system path for file
    """
    f = open(path, 'w')
    f.truncate(0)
    f.close()
    try:
        os.unlink(path)
    except OSError:
        pass


### convert uri request string to list

def uri_to_list(path):
    """
    Parse request path and split uri into list.

    * ``/action/param1/param2`` will be parsed as::

        ['action', 'param1', 'param2']

    """
    try:
        if path[0] == '/':
            path = path[1:]
        if path[-1:] == '/':
            path = path[:-1]
    except IndexError:
        pass
    return path.split('/')




### data object class for storing generic dict key/value pairs

# from web.py
#
# class Storage(dict):
#   """
#   A Storage object is like a dictionary except `obj.foo` can be used
#   in addition to `obj['foo']`.
#
#       >>> o = storage(a=1)
#       >>> o.a
#       1
#       >>> o['a']
#       1
#       >>> o.a = 2
#       >>> o['a']
#       2
#       >>> del o.a
#       >>> o.a
#       Traceback (most recent call last):
#           ...
#       AttributeError: 'a'
#
#   """
#   def __getattr__(self, key):
#       try:
#           return self[key]
#       except KeyError, k:
#           raise AttributeError, k
#
#   def __setattr__(self, key, value):
#       self[key] = value
#
#   def __delattr__(self, key):
#       try:
#           del self[key]
#       except KeyError, k:
#           raise AttributeError, k
#
#   def __repr__(self):
#       return '<Storage ' + dict.__repr__(self) + '>'
#

class DataObject(dict):
    """
    Data object class.

    * based on ``webpy`` dict-like Storage object
    """
    def __init__(self, *args, **kwargs):
        self.add(*args, **kwargs)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError, k:
            raise AttributeError, k

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError, k:
            raise AttributeError, k

    def __repr__(self):
        return '<DataObject ' + dict.__repr__(self) + '>'

    def add(self, *args, **kwargs):
        """
        add({
            'a': 1,
            'b': 3.14,
            'c': 'foo'
        })
        """
        def add_dict(d):
            for name, value in d.items():
                self[name] = value
        add_dict(kwargs)
        for d in args:
            if isinstance(d, (list, tuple)):
                try:
                    for name in d:
                        self[name] = True
                except TypeError:
                    pass
            elif isinstance(d, dict):
                add_dict(d)
            else:
                self[d] = True


### class for configuration storage and management

class Config(object):
    """
    Class for storing configuration settings.
    """
    def __init__(self):
        """
        `namespaces` is list of namespaces defined.
        `config` is DataObject dict for configurations.
        `adhoc_namespace` is name of namespace to add vars to
        when no namespaces are specified in the ``set`` methods.
        """
        self.namespaces = []
        self.config = DataObject()
        self.adhoc_namespace = None

    def add_namespace(self, namespace, data={}):
        """Add a namespace or update an existing one with data."""
        if namespace not in self.namespaces:
            self.namespaces.insert(0, namespace)
            config = DataObject()
            self.config[namespace] = config
        else:
            config = self.get_namespace(namespace)
        if data:
            config.add(data)
        return config

    def get_namespace(self, namespace):
        """Return a config DataObject corresponding to `namespace`."""
        return self.config.get(namespace)

    def update_namespace(self, namespace, data):
        """
        Update the specified `namespace` with data.
        `data` should be dict.
        """
        if namespace in self.namespaces:
            self.config[namespace].add(data)
        else:
            raise AttributeError

    def delete_namespace(self, namespace):
        """Delete a namespace."""
        if namespace in self.namespaces:
            self.namespaces.remove(namespace)
            del self.config[namespace]

    def set_adhoc_namespace(self, namespace):
        """Set the `adhoc_namespace`."""
        self.adhoc_namespace = namespace
        if not namespace in self.namespaces:
            self.add_namespace(namespace)

    def setvar(self, namespace, key, val):
        """Set a var into the specified namespace."""
        try:
            config = self.config[namespace]
            config[key] = val
        except KeyError:
            raise KeyError(namespace)
        return val

    def getvar(self, namespace, key, default_val=None):
        """Get a var from the specified namespace."""
        try:
            config = self.config[namespace]
            return config.get(key, default_val)
        except KeyError:
            raise KeyError(namespace)

    def set(self, key, val, namespace=None):
        """
        Set a var -- if namespace is specified, key-value will be
        added to the namespace, otherwise the config object will
        try to insert it into the `adhoc_namespace` if defined.
        If `adhoc_namespace` is not set, the config object will
        raise a KeyError.
        """
        if not namespace:
            try:
                assert self.adhoc_namespace is not None
                return self.setvar(self.adhoc_namespace, key, val)
            except AssertionError:
                raise KeyError('No ad hoc namespace for setting value.')
        else:
            return self.setvar(namespace, key, val)

    def get(self, key, default_val=None, namespace=None):
        """
        Get a var -- if `namespace` is not specified, the
        config object will loop through the available namespaces
        and return the first match. If no matches are found,
        `default_val` or None is returned. The config object
        will search through namespaces in reverse order of
        definition so the last namespace added is searched first.
        """
        if not namespace:
            for _namespace in self.namespaces:
                config = self.config[_namespace]
                if key in config:
                    return config[key]
        else:
            return self.getvar(namespace, key, default_val)
        return default_val

    def update(self, namespace, data):
        """This is a shorthand for the ``update_namespace`` method."""
        self.update_namespace(namespace, data)



### `safeunicode` and `safestr` from web.py

def safe_unicode(obj, encoding='utf-8'):
    r"""
    Converts any given object to unicode string.

        >>> safeunicode('hello')
        u'hello'
        >>> safeunicode(2)
        u'2'
        >>> safeunicode('\xe1\x88\xb4')
        u'\u1234'
    """
    t = type(obj)
    if t is unicode:
        return obj
    elif t is str:
        return obj.decode(encoding)
    elif t in [int, float, bool]:
        return unicode(obj)
    else:
        if hasattr(obj, '__unicode__'):
            return unicode(obj)
        else:
            return str(obj).decode(encoding)

def safe_str(obj, encoding='utf-8'):
    r"""
    Converts any given object to utf-8 encoded string.

        >>> safestr('hello')
        'hello'
        >>> safestr(u'\u1234')
        '\xe1\x88\xb4'
        >>> safestr(2)
        '2'
    """
    if isinstance(obj, unicode):
        return obj.encode('utf-8')
    elif isinstance(obj, str):
        return obj
    elif hasattr(obj, 'next') and hasattr(obj, '__iter__'): # iterator
        return itertools.imap(safestr, obj)
    else:
        return str(obj)


### simple logger

log_levels = {
            'notset': logging.NOTSET,
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL
        }

log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

def create_log(logname, logfile=None, level='debug', format=log_fmt):
    """
    Create and return simple file logger.

    * level is keyword in `log_levels` (`notset`, `debug`, `info`, etc.)
    * format is format of log entry to output

    :More info: `<http://docs.python.org/library/logging.html>`_

    :param logname: name of log.
    :param logfile: path of log file.
    :param level: log level (see ``log_levels``).
    :param format: log entry format (default is ``log_fmt``).
    :returns: logger object.
    """
    log_level = log_levels.get(level)
    logger = logging.getLogger(logname)
    logger.setLevel(log_level)
    if logfile:
        handler = logging.FileHandler(logfile)
    else:
        handler = logging.StreamHandler()
    handler.setLevel(log_level)
    handler.setFormatter(logging.Formatter(format))
    logger.addHandler(handler)
    return logger
