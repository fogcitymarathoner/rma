from django.conf.urls import patterns, include, url
from commissioned_sites.views import index
from commissioned_sites.views import view
from commissioned_sites.views import SiteUpdateView
from commissioned_sites.views import SiteDeleteView
from commissioned_sites.views import download_site_file
from commissioned_sites.views import download_site_profile_file
from commissioned_sites.views import manage_networks
from commissioned_sites.views import manage_attachments
from commissioned_sites.views import manage_extra_fields
from commissioned_sites.views import create
from django.conf import settings
from django.contrib.auth.decorators import login_required
urlpatterns = patterns('',

    url(r'^$', index, name='commissioned_sites'),
    url(r'show/(?P<id>\d+)$', view, name='view_site'),
    url(r'edit/(?P<id>\d+)$', login_required(SiteUpdateView.as_view()), name='edit_site'),
    url(r'create/$', create, name='create_site'),
    url(r'delete/(?P<id>\d+)$', login_required(SiteDeleteView.as_view()), name='delete_site'),
    url(r'manage_networks/(?P<id>\d+)$', manage_networks, name='site_manage_networks'),
    url(r'manage_attachments/(?P<id>\d+)$', manage_attachments, name='site_manage_attachments'),
    url(r'manage_extra_fields/(?P<id>\d+)$', manage_extra_fields, name='site_manage_extra_fields'),
    url(r''+settings.SUB_URL+'download-commissioned-site-attachment/(?P<id>\d+)$', download_site_file, name='download_commissioned_site_attachment'),
    url(r''+settings.SUB_URL+'download-commissioned-site-profile/(?P<id>\d+)$', download_site_profile_file, name='download_commissioned_site_profile'),
)
