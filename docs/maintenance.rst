Maintenance
===========

Django servers
--------------

Django is used to develop the Full-Stack CRM application. The Django servers are pre-forked wsgi processes waiting for
requests, dispatched from nginx and stay alive after the request

CherryPy Servers
----------------

These are the servers used for UI services on webpages like customer search on the rma list page

Theses servers are collectively restarted with 'supervisord'

Logged In User Sessions
-----------------------

The CRM uses django-redis-session for maintaining user sessions.  The user sessions are wiped off the database in overnight
tasks so CRM users are logged out overnight.  The same Django-Redis session record can be used by the CherryPy apps.

To start these services, start 'supervisord' as root.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  sudo supervisord

To inspect the status of the processes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  sudo supervisorctl
This will list the status of the individual cherrypy apps.

To start the django uwsgi servers, from a dead start
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  cd /home/crm/python_apps/django/rma/deploy && uwsgi --ini uwsgi_prod.ini &
or
  cd /home/crm/python_apps/django/rma_test/deploy &&  uwsgi --ini uwsgi_test.ini  &

To restart a running django uwsgi server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  touch /home/crm/python_apps/django/rma/rma/reload
or
  touch /home/crm/python_apps/django/rma_test/rma/reload

To kill a running django uwsgi
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  cat /home/crm/python_apps/django/rma/rma/pid.txt | xargs kill -9
or
  cat /home/crm/python_apps/django/rma_test/rma/pid.txt | xargs kill -9

Restarting nginx
----------------
  sudo service nginx [restart|reload|stop|start]

CherryPy Applications
---------------------

CherryPy provides RESTFul services to the AJAX applications exposed by Django.

* /customers
* /customers_test

Redis Database Assignments
--------------------------

* 0 customers_test/ customer/rma
* 1 customers/ customer/rma
* 2 sessions storage for all 4 applications, extra-data field keys (suburl:extra_data)

Port Assignments
----------------

* 8080 rma_test
* 8081 rma
* 8082 customers_test
* 8083 customers

Backups
-------

Postgres Database
~~~~~~~~~~~~~~~~~
Everyday at midnight a cron job dumps a date-versioned copy of database into /var/opt/rma/backups .

To effectively use postgres commands, like pgdump and psql, the environment variable PGPASSWORD should be set.  If this
variable isn't set right 'python manage.py dbshell' will ask for the password in settings.py (local_settings.py for
the test site).

To dump the test database logged in as 'crm' (PGPASSWORD) is set right in ~/.bashrc
  pg_dump -U crm rma_test > ~/rma.120512.sql

To load a database dump. (Carefully)
  psql rma < rma.120512.sql

The Repositories
~~~~~~~~~~~~~~~~
A clone of the repository should suffice
as a backup of the production site.  To backup rma_test without a copy of its database, make copies of 'runwsgiserver.sh'
and 'local_settings.py'

Building This Document
----------------------

  cd /home/crm/python_apps/django/rma_test/rma
  fab build_dox_back

Updating Servers
----------------

The production site is under source control so to update to a repository update.::

    cd /home/crm/python_apps/django/rma
    git pull

The test site is not under source control so you must do an rsync from where your IDE is running.::
   # at the development laptop
   cd ~/home/crm/python_apps/django/rma
   fab sync

The GIT Repositories
--------------------

The git repository is in 'crm's' home account under rma.git.  It is under ssh key authentication.  To interact with the
repo copy your public id_rsa keys into crm@10.8.3.10:.ssh/authorized_keys.

To clone the Repository, with public keys installed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For the RMA Django code::

  git clone crm@10.8.3.10:rma.git

For the customer's CherryPy service code::

  git clone crm@10.8.3.10:customers.git

Changing User Password
----------------------

A superuser can change a user's password in the admin panel in the User's app.  Select a user and bring up
the change password dialog.  Look for 'you can change the password using this form.'

Creating Django Superuser
-------------------------

A Django superuser can use the Django control panel to delete records, create records, and give access rights to other
users.

To create a super user.

.. literalinclude:: dox_snippets/createsuperuser.txt
Modules Django uses
-------------------
.. literalinclude:: requirements.txt

Logs for Debugging
------------------
* test site django log /home/crm/python_apps/django/rma_test/rma/log.txt
* production site django log /home/crm/python_apps/django/rma/rma/log.txt
* nginx /var/log/nginx/error.log
* nginx /var/log/nginx/customers.log
* nginx /var/log/nginx/customers_test.log

Nginx
-----
:ref:`nginx_settings`