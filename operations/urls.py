from django.conf.urls import patterns, include, url
from operations.views import move_parts
from operations.views import view_part_to_move
from operations.views import admin_rma_extra_fields
from operations.views import reassign_customers_to_customer_sites
from operations.views import view_customer_site_to_reassign
from operations.views import check_if_site_exists_and_reassign
from operations.views import assign_customer_select_customer
from operations.views import assign_customer_to_site_new_customer
from operations.views import manage_users_roles
from operations.views import manage_user_roles
from operations.views import change_password
urlpatterns = patterns('',
    url(r'move_parts/$', move_parts, name='move_parts'),
    url(r'admin_rma_extra_fields/$', admin_rma_extra_fields, name='admin_rma_extra_fields'),
    url(r'show_part_to_move/(?P<id>\d+)$', view_part_to_move, name='view_part_to_move'),
    url(r'view_customer_site_to_reassign/(?P<id>\d+)$', view_customer_site_to_reassign, name='view_customer_site_to_reassign'),
    url(r'edit_customer_site/(?P<id>\d+)$', check_if_site_exists_and_reassign, name='operations_edit_customer_site'),
    url(r'assign_customer_select_customer/(?P<id>\d+)$', assign_customer_select_customer, name='assign_customer_select_customer'),
    url(r'assign_customer_to_site_new_customer/(?P<id>\d+)$', assign_customer_to_site_new_customer, name='assign_customer_to_site_new_customer'),
    url(r'reassign_customers_to_customer_sites/$', reassign_customers_to_customer_sites, name='reassign_customers_to_customer_sites'),
    url(r'manage_users_roles/$', manage_users_roles, name='manage_users_roles'),
    url(r'manage_user_roles/(?P<id>\d+)$', manage_user_roles, name='manage_user_roles'),
    url(r'change_password/$', change_password, name='change_password'),
)
