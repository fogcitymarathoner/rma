# -*- coding: utf-8 -*-
"""
helpers.email.utils

Helper functions for email module.

* created: 2013-10-27 Kevin Chan <kefin@makedostudio.com>
* updated: 2013-10-27 kchan
"""

from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.template import Context, loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from helpers.txt.utils import tidy_msg


# helper functions

def get_current_site():
    return Site.objects.get_current()


def get_users_in_group(group):
    """Get all users in group by group name."""
    return User.objects.filter(groups__name=group)


# validate email address

def validate_email_address(email):
    """
    from:
    http://stackoverflow.com/questions/3217682/checking-validity-of-email-in-django-python

    :param email: email address to validate
    :returns: True if valid else False
    """
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def render_message(template, context, tidy=True):
    """
    Render a text message using template and context.

    :param template: template
    :param context: context to render template with
    :param tidy: if True, run text through tidy_msg filter (default is True)
    :returns: text
    """
    t = loader.get_template(template)
    msg = t.render(Context(context))
    if tidy:
        msg = tidy_msg(msg)
    return msg
