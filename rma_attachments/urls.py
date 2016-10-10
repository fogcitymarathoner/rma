from django.conf.urls import patterns, include, url

from rma_attachments.views import RmaAttachmentsCreateView
from rma_attachments.views import RmaAttachmentsDeleteView
from rma_attachments.views import SiteAttachmentsCreateView
from rma_attachments.views import SiteAttachmentsDeleteView

from django.contrib.auth.decorators import login_required
urlpatterns = patterns('',
    url(r'create/(?P<id>\d+)$', login_required(RmaAttachmentsCreateView.as_view()), name='create_rma_attachment'),
    url(r'delete/(?P<id>\d+)$', login_required(RmaAttachmentsDeleteView.as_view()), name='delete_rma_attachment'),
    url(r'site_attachment_create/(?P<id>\d+)$', login_required(SiteAttachmentsCreateView.as_view()), name='create_site_attachment'),
    url(r'site_attachment_delete/(?P<id>\d+)$', login_required(SiteAttachmentsDeleteView.as_view()), name='delete_site_attachment'),
)
