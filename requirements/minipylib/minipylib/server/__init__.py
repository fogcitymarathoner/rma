# -*- coding: utf-8 -*-
"""
minipylib.server

The **minipylib.server** module contains adaptor classes to run a wsgi server.
The module is independent of all the other files in the minipy package
so you can include it for only the server adaptor you need to run a
fully functional python webserver.

Included in the minipylib distribution is a copy of the threaded wsgiserver
from `CherryPy <http://www.cherrypy.org/>`_. The *wsgiserver* is the default
server for the *minipylib.server* module.

``server_registry`` is dict of available servers.

* Unimportable servers will not be entered into the registry.
* The default server is CherryPy's wsgiserver (included in wsgiserver directory)

Supported servers:

* wsgiserver: CherryPy wsgiserver (included in minipylib)
* cherrypy: CherryPy wsgiserver from package
* fapws: fapws3
* simple_server: python built-in wsgiref.simple_server
* uwsgi: uwsgi
* eventlet: Linden Lab eventlet
* gevent_pywsgi: gevent
* bjoern: bjoern

Copyright (c) 2008-2011 kevin chan <kefin@makedostudio.com>

* created: 2009-09-11 kevin chan <kefin@makedostudio.com>
* updated: 2012-12-19 kchan
"""

import sys
import os

DEFAULT_SERVER = 'wsgiserver'
DEFAULT_SERVER_HOST = '127.0.0.1'
DEFAULT_SERVER_PORT = 8080

DEFAULT_SERVER_USER = 'nobody'
DEFAULT_SERVER_GROUP = 'nogroup'

# default number of threads for CherryPy wsgiserver
DEFAULT_THREADS = 10



#######################################################################
# web server configurations
#######################################################################


class ServerConfig(object):
    pass


def get_server_config(**params):
    """
    Return a ServerConfig object with info for a server.
    """
    c = ServerConfig()
    c.server = params.get('server', DEFAULT_SERVER)
    default_bind_addr = (DEFAULT_SERVER_HOST, DEFAULT_SERVER_PORT,)
    c.bind_addr = params.get('bind_addr', default_bind_addr)
    c.host_name = params.get('host_name', '')
    c.server_user = params.get('server_user', DEFAULT_SERVER_USER)
    c.server_group = params.get('server_group', DEFAULT_SERVER_GROUP)
    c.app = params.get('app')
    c.params = params
    return c


#######################################################################
# server registry functions
#######################################################################


server_registry = {}


def register_server(cls):
    """
    Register a wsgi server in the server registry.

    :param name: is keyword to identify server
    :param cls: is class definition for server adaptor
    """
    server = getattr(cls, 'name')
    if server:
        server_registry[server] = cls


def get_server(server, config):
    """
    Return Server instance corresponding to name.

    :param server: keyword name of wsgi server
    :param config: config is ServerConfig object
    """
    if server not in server_registry:
        server = DEFAULT_SERVER
    return server_registry[server](config)


def get_server_list():
    """
    Return server registry.
    """
    return server_registry


def get_web_server(**params):
    """
    Return a Server object according to supplied params.

    To run server::

        app = my_wsgi_app
        bind_addr = ('127.0.0.1', 8080)
        server = get_web_server(server='wsgiserver', bind_addr=bind_addr, app=app)
        server.run()

    """
    return get_server(params.get('server'), get_server_config(**params))



#######################################################################
# server template
#######################################################################

class Server(object):
    """
    Template for wsgi server variant
    """
    name = None

    def __init__(self, config):
        """
        :param config: config is a ServerConfig object.
        """
        self.config = config
        self.server = config.server
        user = config.server_user
        group = config.server_group
        if user and group:
            change_uid_gid(user, group)

    def run(self):
        """
        Runs wsgi server. Subclass should override.
        """
        pass

    def stop(self):
        """
        Stops wsgi server. Not all wsgi servers have a stop method.
        To stop server running as daemon, send kill signal to script.
        """
        pass



#######################################################################
# wsgiref.simple_server
# * python bulit-in wsgiref.simple_server (only available in
#   Python 2.5 or above).
#######################################################################

if sys.hexversion >= 0x2050000:

    from wsgiref.simple_server import make_server

    @register_server
    class SimpleServer(Server):
        """
        Python bulit-in ``wsgiref.simple_server``.
        """
        name = 'simple_server'

        def run(self):
            host, port = self.config.bind_addr
            self.server = make_server(host, port, self.config.app)
            try:
                self.server.serve_forever()
            except KeyboardInterrupt:
                self.stop()



#######################################################################
# local copy of CherryPy wsgiserver (included in minipylib)
#######################################################################

@register_server
class WsgiServer(Server):
    """
    CherryPy wsgiserver

    * This module is copied from the Cherrypy distribution.
    """
    name = 'wsgiserver'

    def run(self):
        import wsgiserver
        self.server = wsgiserver.CherryPyWSGIServer(
                        self.config.bind_addr,
                        self.config.app,
                        server_name=self.config.host_name,
                        numthreads=self.config.params.get('threads', DEFAULT_THREADS))
        try:
            self.server.start()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.server.stop()



#######################################################################
# CherryPy wsgiserver
# info: http://www.cherrypy.org/
#######################################################################

# add the official cherrypy server from the package

try:
    from cherrypy import wsgiserver as cherry

    @register_server
    class CherryPyServer(Server):
        """
        CherryPy wsgiserver

        :source: http://www.cherrypy.org/
        """
        name = 'cherrypy'

        def run(self):
            self.server = cherry.CherryPyWSGIServer(
                            self.config.bind_addr,
                            self.config.app,
                            server_name=self.config.host_name,
                            numthreads=self.config.params.get('threads', DEFAULT_THREADS))
            try:
                self.server.start()
            except KeyboardInterrupt:
                self.stop()

        def stop(self):
            self.server.stop()


except ImportError:
    pass



#######################################################################
# fapws3
# info: http://www.fapws.org/
#######################################################################

try:
    import fapws._evwsgi as evwsgi

    @register_server
    class FapwsServer(Server):
        """
        FAPWS3 (Fast Asynchronous Python Web Server)

        :source: http://www.fapws.org/
        :source: https://github.com/william-os4y/fapws3
        """
        name = 'fapws'

        def run(self):
            from fapws import base
            try:
                # since we don't use threads, internal checks are no more required
                sys.setcheckinterval=100000
                # fapws evwsgi.start() seems to ignore the port
                # if it's a number and requires it to be a string,
                # so we cast it here to get it to work correctly.
                host, port = self.config.bind_addr
                evwsgi.start(host, str(port))
                evwsgi.set_base_module(base)
                evwsgi.wsgi_cb(('', self.config.app))
                evwsgi.set_debug(0)
                evwsgi.run()
            except KeyboardInterrupt:
                self.stop()

except ImportError:
    pass



#######################################################################
# uwsgi
# info: http://projects.unbit.it/uwsgi/
#######################################################################

# * uswgi serves differently than the other wsgi servers. It requires
#   a dict with url routes mapped to callables. Here, we just set the
#   uwsgi.application with a dummy dict that funnels everything to the
#   web app.
# * See: http://projects.unbit.it/uwsgi/wiki/ApplicationsDict
# * All other uswgi options are set in XML file loaded by uswgi when
#   invoked as daemon so we don't have to do any configuration here.

try:
    import uwsgi

    @register_server
    class UwsgiServer(Server):
        """
        uWSGI: fast (pure C), self-healing, developer-friendly WSGI server

        :source: http://projects.unbit.it/uwsgi/
        """
        name = 'uwsgi'

        def __init__(self, config):
            Server.__init__(self, config)
            uwsgi.applications = {'': self.config.app}

except ImportError:
    pass



#######################################################################
# Linden Lab eventlet
# info: http://eventlet.net/
#######################################################################

try:
    import eventlet

    @register_server
    class EventletServer(Server):
        """
        Linden Lab eventlet

        :source: http://eventlet.net/
        """
        name = 'eventlet'

        def run(self):
            from eventlet import wsgi
            wsgi.server(eventlet.listen(self.config.bind_addr), self.config.app)

except ImportError:
    pass



#######################################################################
# gevent pywsgi server
# info: http://www.gevent.org/
#######################################################################

try:
    from gevent.pywsgi import WSGIServer as gevent_pywsgi

    @register_server
    class GeventPYWsgiServer(Server):
        """
        gevent.pywsgi.WSGIServer

        :source: http://www.gevent.org/
        """
        name = 'gevent_pywsgi'

        def run(self):
            self.server = gevent_pywsgi(self.config.bind_addr, self.config.app)
            try:
                self.server.serve_forever()
            except:
                pass

except ImportError:
    pass



#######################################################################
# bjoern server
# info: https://github.com/jonashaag/bjoern
#######################################################################

try:
    import bjoern

    @register_server
    class BjoernServer(Server):
        """
        bjoern

        :source: https://github.com/jonashaag/bjoern
        """
        name = 'bjoern'

        def run(self):
            host, port = self.config.bind_addr
            bjoern.listen(self.config.app, host, port)
            bjoern.run()

except ImportError:
    pass



#######################################################################
# wsgi apps
#######################################################################

### test_app - generic test app for testing wsgi server

if sys.hexversion >= 0x2050000:
    from wsgiref.simple_server import demo_app
    test_app = demo_app
else:
    def test_app(environ, start_response):
        """
        Simplest possible application object
        * from PEP 333 - http://www.python.org/dev/peps/pep-0333/
        """
        status = '200 OK'
        response_headers = [('Content-type','text/plain')]
        start_response(status, response_headers)
        return ['Hello world!\n']


### get_django_app - get app for serving a django project

def get_django_app(server):
    """
    Return wsgi app serving django project.

    `server` is server type:

    * fapws
    * wsgiserver
    * simple_server
    * uwsgi
    """
    try:
        import django
        from django.core.handlers.wsgi import WSGIHandler
    except ImportError:
        class WSGIHandler(object):
            def __call__(self, environ, start_response):
                status = '200 OK'
                response_headers = [('Content-type','text/plain')]
                start_response(status, response_headers)
                return ['Unable to import django. Please check your installation.\n']

    if server == 'fapws':
        # from fapws.contrib.django_handler
        def django_handler(environ, start_response):
            wsgi_handler = WSGIHandler()
            response = wsgi_handler(environ, start_response)
            try:
                if django.VERSION[0] == 0:
                    for key, val in response.headers.items():
                        start_response.response_headers[key] = val
                else:
                    for key, val in response._headers.values():
                        start_response.response_headers[key] = val
                start_response.cookies = response.cookies
                return [response.content]
            except (NameError, AttributeError):
                return response
        return django_handler
    else:
        return WSGIHandler()



#######################################################################
# utility functions
# * adapted from django-cerise and django-cpserver
# ** http://xhtml.net/scripts/Django-CherryPy-server-DjangoCerise
# ** http://github.com/lincolnloop/django-cpserver
#######################################################################

def change_uid_gid(uid, gid=None):
    """Try to change UID and GID to the provided values.
    UID and GID are given as names like 'nobody' not integer.

    :Source: `http://mail.mems-exchange.org/durusmail/quixote-users/4940/1/ <http://mail.mems-exchange.org/durusmail/quixote-users/4940/1/>`_
    """
    if not os.geteuid() == 0:
        # Do not try to change the gid/uid if not root.
        return
    (uid, gid) = get_uid_gid(uid, gid)
    os.setgid(gid)
    os.setuid(uid)

def get_uid_gid(uid, gid=None):
    """Try to change UID and GID to the provided values.
    UID and GID are given as names like 'nobody' not integer.

    :Source: `http://mail.mems-exchange.org/durusmail/quixote-users/4940/1/ <http://mail.mems-exchange.org/durusmail/quixote-users/4940/1/>`_
    """
    import pwd, grp
    uid, default_grp = pwd.getpwnam(uid)[2:4]
    if gid is None:
        gid = default_grp
    else:
        try:
            gid = grp.getgrnam(gid)[2]
        except KeyError:
            gid = default_grp
    return (uid, gid)



#######################################################################
# Webserver class to run server.
# * class interface to create web server for compatibility with old code.
#######################################################################

class Webserver(object):
    """
    Class to manage wsgi server for web application.

    Params should include keys in the default server params below::

        app
        server
        bind_addr
        host_name
        server_user
        server_group

    Default settings::

        DEFAULT_SERVER = 'wsgiserver'
        DEFAULT_SERVER_HOST = '127.0.0.1'
        DEFAULT_SERVER_PORT = 8080

        DEFAULT_SERVER_USER = 'nobody'
        DEFAULT_SERVER_GROUP = 'nobody'

    How to use

    * in your **index.py**, create instance of Webserver and provide
      appropriate parameters for your setup::

        server = Webserver(
                app=wsgi_application,
                server=WSGI_SERVER,
                bind_addr=(WSGI_SERVER_HOST, WSGI_SERVER_PORT)
        )

    :note: wsgi_application is your wsgi application.

    * run server::

        if __name__=="__main__":
            server.run()

    """
    def __init__(self, **params):
        # older invocation code uses 'wsgi_server' instead of 'server'
        # so we set 'server' here so get_server_config will use
        # the correct server.
        if not 'server' in params:
            params['server'] = params.get('wsgi_server')
        c = get_server_config(**params)
        self.server = get_server(c.server, c)

    def run(self):
        self.server.run()

    def stop(self):
        self.server.stop()
