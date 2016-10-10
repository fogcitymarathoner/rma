__author__ = 'marc'
from django import template
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

register = template.Library()

@register.filter(name='clean_html_address')
def clean_html_address(site):
    """

    :param site:
    :return:
    """
    s = MLStripper()
    s.feed(site.address)
    return s.get_data()