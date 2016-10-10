__author__ = 'marc'
from django import template
from return_merchandise_authorizations.settings import SHIPPING_CHOICES

register = template.Library()

@register.filter(name='shipping_method')
def shipping_method(rma):
    """

    :param site:
    :return:
    """
    for p in SHIPPING_CHOICES:
        if str(p[0]) == rma.shipping:
            return p[1]


