# -*- coding: utf-8 -*-
"""
helpers.email.emails

Functions to help send emails.

* created: 2011-02-15 Kevin Chan <kefin@makedostudio.com>
* updated: 2013-10-27 kchan
"""

from django.core.mail import (
    mail_admins,
    send_mass_mail,
    EmailMultiAlternatives
)
from django.template.loader import render_to_string

from garage import get_setting as _s
from helpers.txt.utils import html_to_text

from .settings import (
    get_template_for as _template,
    get_msg as _msg,
)
from .utils import (
    get_current_site,
    get_users_in_group,
    validate_email_address,
)


# email a list of individuals

def send_email(subject, message, recipient_list, from_email=None,
               fail_silently=False, connection=None):
    """
    Sends a message to each recipient in recipient list.

    :param subject: email subject
    :param messge: email message/body
    :param recipient_list: list/tuple of recipient emails
    :param from_email: email address for "from:" (defaults to
        SERVER_EMAIL or DEFAULT_FROM_EMAIL in settings)
    :param fail_silently: unused
    :param connection: unused
    """
    if not from_email:
        from_email = _s('SERVER_EMAIL') or _s('DEFAULT_FROM_EMAIL')
    try:
        subj = unicode(subject)
    except UnicodeDecodeError:
        subj = subject.decode('utf8')
    datatuple = [(subj, message, from_email, [recipient],) \
                 for recipient in recipient_list]
    send_mass_mail(datatuple)


# send debug email to admins

def send_debug_email(subject, message):
    """
    Send debug email to admins.

    :param subject: email subject
    :param messge: email message/body
    """
    if not subject:
        site = get_current_site()
        subj = _s('DEBUG_MSG_SUBJECT') or _msg('subject_debug_msg')
        subject = '%s: %s' % (site.name, subj)
    mail_admins(subject, message, fail_silently=True)


# send email to members in group

def send_email_to_group(group, subject, message, fail_silently=False):
    """
    Send emails to a group.

    * FIXME: this function should be deprecated and deleted from
      helpers.email (functionality is redundant -- use send_email
      instead).

    :param group: group name or list of recipients
    :param subject: email subject
    :param message: email message/body
    :param fail_silently: if False, will send debug email to admins
    """
    if isinstance(group, basestring):
        members = get_users_in_group(group)
        recipients = [user.email for user in members if user.email]
    elif isinstance(group, (list, tuple)):
        recipients = group
    try:
        assert recipients
    except AssertionError:
        if not fail_silently:
            template = _s('NOTIFICATION_FAILED_TEMPLATE') \
                       or _template('notification_failed')
            debug_subj = _s('GROUP_EMAIL_FAILED_SUBJECT') \
                         or _msg('subject_group_email_failed')
            emsg = _msg('msg_group_email_failed')
            debug_msg = '%s: %s' % (emsg, group)
            site_name = get_current_site().name
            context = {
                'debug_message': debug_msg,
                'subject': subject,
                'recipients': recipients,
                'message': message,
                'site_name': site_name
            }
            msg = render_to_string(template, context)
            admins = _s('ADMINS')
            recipients = [email for name, email in admins]
            send_email(debug_subj, msg, recipients, fail_silently=False)
    else:
        send_email(subject, message, recipients, fail_silently=True)


# send html email

def send_html_email(subject,
                    recipient_list,
                    template,
                    context,
                    from_email=None,
                    text_content=None):
    """
    Send email with text and html versions.

    Reference link:
    https://docs.djangoproject.com/en/dev/topics/email/

    :param subject: email subject
    :param recipient_list: list/tuple of recipient emails
    :param template: path to html email template
    :param context: context for html email template
    :param from_email: email address for "from:" (defaults to
        SERVER_EMAIL or DEFAULT_FROM_EMAIL in settings)
    :param text_content: content for plain text version of email
    """
    if not from_email:
        from_email = _s('SERVER_EMAIL') or _s('DEFAULT_FROM_EMAIL')
    try:
        subj = unicode(subject)
    except UnicodeDecodeError:
        subj = subject.decode('utf8')

    html_content = render_to_string(template, context)
    if not text_content:
        text_content = html_to_text(html_content)

    # create the email and attach the HTML version
    # * html content will be in EmailMessage's 'alternative' attribute
    #   list
    msg = EmailMultiAlternatives(subj,
                                 text_content,
                                 from_email,
                                 recipient_list)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
