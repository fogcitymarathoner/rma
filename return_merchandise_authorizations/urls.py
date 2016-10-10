from django.conf.urls import patterns, include, url
from django.conf import settings
from return_merchandise_authorizations.views import index
from return_merchandise_authorizations.views import view
from return_merchandise_authorizations.views import logout
from return_merchandise_authorizations.views import rma_login
from return_merchandise_authorizations.views import RmaUpdateView
from return_merchandise_authorizations.views import create
from return_merchandise_authorizations.views import RmaDeleteView
from return_merchandise_authorizations.views import RmaApproveView
from return_merchandise_authorizations.views import manage_items
from return_merchandise_authorizations.views import manage_attachments
from return_merchandise_authorizations.views import manage_extra_fields
from return_merchandise_authorizations.views import download_rma_file
from django.contrib.auth.decorators import login_required
urlpatterns = patterns('',
    url(r'^$', index, name='home_page'),
    url(r'show/(?P<id>\d+)$', view, name='view_rma'),
    url(r'logout/$', logout, name='rma_logout'),
    url(r'login/$', rma_login, name='rma_login'),
    url(r'create/$', create, name='create_rma'),
    url(r'approve/(?P<id>\d+)$', login_required(RmaApproveView.as_view()), name='approve_rma'),
    url(r'edit/(?P<id>\d+)$', login_required(RmaUpdateView.as_view()), name='edit_rma'),
    url(r'delete/(?P<id>\d+)$', login_required(RmaDeleteView.as_view()), name='delete_rma'),
    url(r'manage_items/(?P<id>\d+)$', manage_items, name='manage_items'),
    url(r'manage_attachments/(?P<id>\d+)$', manage_attachments, name='manage_attachments'),
    url(r'manage_extra_fields/(?P<id>\d+)$', manage_extra_fields, name='manage_extra_fields'),
    url(r''+settings.SUB_URL+'download-rma-attachment/(?P<id>\d+)$', download_rma_file, name='download_rma_attachment'),
)
