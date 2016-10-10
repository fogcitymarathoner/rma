from django.conf.urls import patterns, include, url

from site_attachments.views import SiteAttachmentsCreateView
from site_attachments.views import SiteAttachmentsDeleteView

from django.contrib.auth.decorators import login_required
urlpatterns = patterns('',
    url(r'create/(?P<id>\d+)$', login_required(SiteAttachmentsCreateView.as_view()), name='create_site_attachment'),
    url(r'delete/(?P<id>\d+)$', login_required(SiteAttachmentsDeleteView.as_view()), name='delete_site_attachment'),
)
