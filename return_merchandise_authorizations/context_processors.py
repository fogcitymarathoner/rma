__author__ = 'marc'
# -*- coding: utf-8 -*-
"""
context_processor

Context processors for project.

"""

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse, NoReverseMatch

from garage import get_setting as _s

def project_context(request):
    """
    THIS DOES NOT WORK
    default context for project templates.
    """
    user = request.user
    # site
    site = Site.objects.get_current()

    # storage configurations
    use_remote_storage = _s('USE_REMOTE_STORAGE', False)

    # media paths and urls
    site_title = _s('SITE_TITLE')
    static_root = _s('STATIC_ROOT')
    static_url = _s('STATIC_URL')
    local_static_url = _s('LOCAL_STATIC_URL', static_url)
    media_root = _s('MEDIA_ROOT')
    media_url = _s('MEDIA_URL')
    local_media_url = _s('LOCAL_MEDIA_URL', media_url)
    resources_root = _s('RESOURCES_ROOT', static_root)
    resources_url = _s('RESOURCES_URL', static_url)
    local_resources_url = _s('LOCAL_RESOURCES_URL', local_static_url)


    try:
        home_url = _s('HOME_URL') or reverse('home')
        assert home_url
    except (NoReverseMatch, AssertionError):
        home_url = '/'

    search_url = _s('SEARCH_URL', '/search/')
    return {
        'settings': settings,
        'use_remote_storage': use_remote_storage,
        'static_root': static_root,
        'static_url': static_url,
        'local_static_url': local_static_url,
        'media_root': media_root,
        'media_url': media_url,
        'local_media_url': local_media_url,
        'resources_root': resources_root,
        'resources_url': resources_url,
        'local_resources_url': local_resources_url,
        'home_url': home_url,
        'search_url': search_url,
        'site_name': site.name,
        'site_domain': site.domain,
        'site_title': site_title,
    }

def site_title(request):
    return {'site_title': settings.SITE_TITLE}
def sub_url(request):
    return {'sub_url': settings.SUB_URL}
def customers_service_url(request):
    return {'customers_service_url': settings.CUSTOMERS_SERVICE_URL}