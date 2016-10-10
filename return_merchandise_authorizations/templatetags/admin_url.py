__author__ = 'marc'
from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def admin_panel_url():
    u = '/'+settings.SUB_URL+'admin'
    return '<a href="%s">Admin</a>'%u