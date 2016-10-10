from django.conf.urls import patterns, include, url

from customers.views import index
from customers.views import index_customer_sites
from customers.views import view
from customers.views import view_site
from customers.views import CustomerUpdateView
from customers.views import CustomerCreateView
from customers.views import CustomerDeleteView
from customers.views import CustomerSiteUpdateView
from customers.views import CustomerSiteCreateCustomerView
from customers.views import CustomerSiteCreateView
from customers.views import CustomerSiteDeleteView

from django.contrib.auth.decorators import login_required
urlpatterns = patterns('',
    url(r'^$', index, name='list_customers'),
    url(r'sites/$', index_customer_sites, name='list_customer_sites'),
    url(r'show/(?P<id>\d+)$', view, name='view_customer'),
    url(r'show_site/(?P<id>\d+)$', view_site, name='view_customer_site'),
    url(r'create/$', login_required(CustomerCreateView.as_view()), name='create_customer'),
    url(r'create_site/$', login_required(CustomerSiteCreateView.as_view()), name='create_customer_site'),
    url(r'create_site_for_customer/(?P<customer_id>\d+)$', login_required(CustomerSiteCreateCustomerView.as_view()), name='create_customer_site_for_customer'),
    url(r'delete/(?P<id>\d+)$', login_required(CustomerDeleteView.as_view()), name='delete_customer'),
    url(r'delete_site/(?P<id>\d+)$', login_required(CustomerSiteDeleteView.as_view()), name='delete_customer_site'),
    url(r'edit/(?P<id>\d+)$', login_required(CustomerUpdateView.as_view()), name='edit_customer'),
    url(r'edit_site/(?P<id>\d+)$', login_required(CustomerSiteUpdateView.as_view()), name='edit_customer_site'),
)
