# -*- coding: utf-8 -*-
"""
helpers.forms.utils

Form utilities.

* created: 2012-07-09 kevin chan <kefin@makedostudio.com>
* updated: 2013-04-28 kchan
"""

from django.template import Context, loader
from django.contrib.sites.models import Site

from helpers.email.emails import send_email_to_group



# helper functions

def get_current_site():
    return Site.objects.get_current()


def get_form(form, *args):
    if len(args) == 0:
        return form(auto_id=True)
    else:
        return form(*args)


def populate_form(form_class, data, processor=None):
    """
    Populate a form based on submitted values.

    :param form_class: the class to use to instantiate form
    :param data: submitted form data
    :param processor: a callable to process data before instantiating
    :returns: form object
    """
    if callable(processor):
        data = processor(data)
    return get_form(form_class, data)


def send_submission_notification(group, subject, data, template, extra_context={}):
    """
    Handler functon to send emails to group when there's a new submission.
    """
    if not data:
        return
    t = loader.get_template(template)
    c = {
        'data': data,
        'site': get_current_site()
        }
    try:
        c.update(extra_context)
    except TypeError:
        pass
    message = t.render(Context(c))
    send_email_to_group(group, subject, message, fail_silently=False)
