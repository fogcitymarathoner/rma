__author__ = 'marc'
from django import template
from return_merchandise_authorizations.settings import Yes

register = template.Library()

@register.filter(name='software_upgraded')
def software_upgraded(site):
    """

    :param site:
    :return:
    """
    if site.software_upgraded == Yes:
        return 'YES'
    else:
        return 'NO'


