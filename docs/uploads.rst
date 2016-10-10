
Uploads - Attachments to RMA and Commissioned Sites
===================================================

Django has a security hole with it's default content uploading.  Django by default uploads to a public area and
offloads the serving of that uploaded content to the web server.

You can upload attachments in the Django Control Panel, but you cannot download.

Downloads are enabled by controller actions instead of urls straight to the STATIC_DIR exposed publically by Nginx.

Enlighted Uploaded File Storage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Enlighted attachment uploads go to '/var/opt/rma/attachments/::

    /var/opt/rma
    ├── attachments
    │   ├── commissioned_sites
    │   │   ├── production
    │   │   └── test
    │   └── rma
    │       ├── production
    │       └── test
