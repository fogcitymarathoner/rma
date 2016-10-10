from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
urlpatterns = patterns('',
    url(r'^'+settings.SUB_URL+'$', include('return_merchandise_authorizations.urls')),
    url(r'^'+settings.SUB_URL+'rma/', include('return_merchandise_authorizations.urls')),
    url(r'^'+settings.SUB_URL+'parts/', include('parts.urls')),
    url(r'^'+settings.SUB_URL+'returned_items/', include('returned_items.urls')),
    url(r'^'+settings.SUB_URL+'services/', include('services.urls')),
    url(r'^'+settings.SUB_URL+'rma_attachments/', include('rma_attachments.urls')),
    url(r'^'+settings.SUB_URL+'networks/', include('site_networks.urls')),
    url(r'^'+settings.SUB_URL+'commissioned-sites/', include('commissioned_sites.urls')),
    url(r'^'+settings.SUB_URL+'operations/', include('operations.urls')),
    url(r'^'+settings.SUB_URL+'customers/', include('customers.urls')),
    url(r'^'+settings.SUB_URL+'reports/', include('reports.urls')),
    url(r'^'+settings.SUB_URL+'admin/', include(admin.site.urls)),
)
