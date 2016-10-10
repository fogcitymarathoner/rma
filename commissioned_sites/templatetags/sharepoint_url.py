__author__ = 'marc'
from django import template
from django.conf import settings

import unicodedata
import urllib
register = template.Library()

@register.filter(name='share_point_url')
def share_point_url(site):
    """

    :param site:
    :return:
    """

    filename_cleaned = unicodedata.normalize('NFKD', site.sharepoint_origin_url).encode('ascii','ignore')
    first_part = '<a href="JavaScript:newPopup(\''+'https://enlighted.sharepoint.com/support/_layouts/15/FormServer.aspx?XmlLocation=/support/CommissionedSites/'
    middle_part = urllib.quote_plus(filename_cleaned)
    last_part = '&ClientInstalled=true&DefaultItemOpen=1&Source=https%3A%2F%2Fenlighted%2Esharepoint%2Ecom%2Fsupport%2FCommissionedSites%2FForms%2FAllItems%2Easpx\');">SharePoint</a>'
    res = first_part + middle_part + last_part
    return res
