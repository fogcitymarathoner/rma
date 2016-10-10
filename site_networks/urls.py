from django.conf.urls import patterns, include, url

from site_networks.views import NetworkCreateView
from site_networks.views import NetworkUpdateView
from site_networks.views import NetworkDeleteView
from django.contrib.auth.decorators import login_required
urlpatterns = patterns('',
    url(r'create/(?P<id>\d+)$', login_required(NetworkCreateView.as_view()), name='create_network'),
    url(r'edit/(?P<id>\d+)$', login_required(NetworkUpdateView.as_view()), name='edit_network'),
    url(r'delete/(?P<id>\d+)$', login_required(NetworkDeleteView.as_view()), name='delete_network'),
)
