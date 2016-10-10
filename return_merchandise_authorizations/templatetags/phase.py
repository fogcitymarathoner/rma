__author__ = 'marc'
from django import template
from return_merchandise_authorizations.settings import PHASE_CHOICES

register = template.Library()

@register.filter(name='phase')
def phase(rma):
    """

    :param site:
    :return:
    """
    for p in PHASE_CHOICES:
        if p[0] == rma.phase:
            return p[1]


