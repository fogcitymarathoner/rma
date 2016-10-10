

Python Settings
===============

The RMA django server (/rma) is setup to run under the directory ``/home/crm/python_apps/django/rma``

The RMA django server (/rma_test) is setup to run under the directory ``/home/crm/python_apps/django/rma_test``
This test server runs differently than production with the inclusion of the ``local_settings.py`` file, which is not
in source control and is not used in production

.. literalinclude:: rma/local_settings.py