REST Services
=============

UI elements requiring database querying for customer information in dropdown lists like customer search on a few characters
make their queries through RESTful calls to a thin CherryPy application that queries a Redis cache that is updated daily
from SalesForce.

/customers_test
~~~~~~~~~~~~~~~

Feeds the /rma_test django application.

/customers
~~~~~~~~~~

Feeds the /rma django production application.