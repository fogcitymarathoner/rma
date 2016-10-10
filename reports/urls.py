from django.conf.urls import patterns, include, url

from reports.views import parts
from reports.views import parts_all_time
from reports.views import parts_by_part_number
from reports.views import report_parts_in_life
from reports.views import report_parts_out_of_life
from reports.views import unapproved_rmas
from reports.views import report_return_inventory
from reports.views import report_customer_rma
from reports.views import report_customer_sites
from reports.views import parts_by_quarter_by_site
from reports.views import show_sites_rmas
from reports.views import show_rma
from reports.views import report_user_roles
from reports.views import operation_not_allowed
urlpatterns = patterns('',
    url(r'parts/$', parts, name='report_parts'),
    url(r'parts_all_time/$', parts_all_time, name='report_parts_all_time'),
    url(r'parts_by_part_number/$', parts_by_part_number, name='report_parts_by_part_number'),
    url(r'report_parts_by_quarter_by_site/$', parts_by_quarter_by_site, name='report_parts_by_quarter_by_site'),
    url(r'report_parts_in_life/$', report_parts_in_life, name='report_parts_in_life'),
    url(r'report_parts_out_of_life/$', report_parts_out_of_life, name='report_parts_out_of_life'),
    url(r'report_unapproved_rmas/$', unapproved_rmas, name='report_unapproved_rmas'),
    url(r'report_return_inventory/$', report_return_inventory, name='report_return_inventory'),
    url(r'report_customer_rma/$', report_customer_rma, name='report_customer_rma'),
    url(r'report_customer_sites/$', report_customer_sites, name='report_customer_sites'),
    url(r'report_user_roles/$', report_user_roles, name='report_user_roles'),
    url(r'show_sites_rmas/(?P<id>\d+)$', show_sites_rmas, name='show_sites_rmas'),
    url(r'show_rma/(?P<id>\d+)$', show_rma, name='show_rma'),
    url(r'operation_not_allowed/$', operation_not_allowed, name='operation_not_allowed'),
)
