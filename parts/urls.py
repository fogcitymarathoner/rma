from django.conf.urls import patterns, include, url
from parts.views import index
from parts.views import view
from parts.views import PartUpdateView
from parts.views import PartUpdateOpsView
from parts.views import PartCreateView
from parts.views import PartDeleteView
from parts.views import PartDeleteOpsView
from django.contrib.auth.decorators import login_required
urlpatterns = patterns('',
    url(r'^$', index, name='list_parts'),
    url(r'show/(?P<id>\d+)$', view, name='view_part'),
    url(r'create/$', login_required(PartCreateView.as_view()), name='create_part'),
    url(r'delete/(?P<id>\d+)$', login_required(PartDeleteView.as_view()), name='delete_part'),
    url(r'delete-ops/(?P<id>\d+)$', login_required(PartDeleteOpsView.as_view()), name='delete_part_ops'),
    url(r'edit/(?P<id>\d+)$', login_required(PartUpdateView.as_view()), name='edit_part'),
    url(r'edit-ops/(?P<id>\d+)$', login_required(PartUpdateOpsView.as_view()), name='edit_part_ops'),
)
