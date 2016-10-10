__author__ = 'marc'

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from return_merchandise_authorizations.models import Item
from commissioned_sites.models import Network
import os
from django.conf import settings

from customers.models import Customer
from customers.models import CustomerCompany
def mail_new_rma_message(rma):

    plaintext = get_template('return_merchandise_authorizations/email.txt')
    htmly     = get_template('return_merchandise_authorizations/email.html')

    d = Context({
        'username': rma.last_modified_by.username,
        'rma': rma,
        'items': Item.objects.filter(rma=rma),
    })

    subject = 'RMA:%s %s'%(rma.customer.name, rma.reference_number)
    from_email = settings.EMAIL_HOST_USER
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [settings.RMA_RECIPIENT_EMAIL])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def mail_new_site_message(site):

    plaintext = get_template('return_merchandise_authorizations/email_new_site.txt')
    htmly     = get_template('return_merchandise_authorizations/email_new_site.html')

    d = Context({
        'username': site.last_modified_by.username,
        'site': site,
        'networks': Network.objects.filter(site=site),
    })

    subject = 'Site:%s %s'%(site.name, site.date)
    from_email = settings.EMAIL_HOST_USER
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [settings.RMA_RECIPIENT_EMAIL])

    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)


def mail_approved_rma_message(rma):

    plaintext = get_template('return_merchandise_authorizations/email.html')
    htmly     = get_template('return_merchandise_authorizations/email_approval.html')

    d = Context({
        'username': rma.last_modified_by.username,
        'rma': rma,
        'items': Item.objects.filter(rma=rma),
    })

    subject = 'RMA:%s %s APPROVED'%(rma.customer.name, rma.reference_number)
    from_email = settings.EMAIL_HOST_USER
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [settings.RMA_RECIPIENT_EMAIL])
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)

def site_autocomplete_dropdown_selections():

    sites = Customer.objects.exclude(customer__company_name='UNKNOWNCOMPANY').order_by('customer__company_name'). \
        order_by('name')
    cchoices = ''
    for y in sites:
        cchoices += '{ company_name: "%s", site_name: "%s", company_id: "%s", value: "%s: %s-%s", label: "%s-%s"' %\
                    (y.customer.company_name, y.name, y.customer.id, y.id, y.customer.company_name, y.name, y.customer.company_name, y.name)+'},'
    return '['+cchoices+']'
def customer_autocomplete_dropdown_selections():

    customers = CustomerCompany.objects.exclude(company_name='UNKNOWNCOMPANY').order_by('company_name')

    cchoices = ''
    for y in customers:
        cchoices += '{ value: "'+str(y.id)+': %s", label: "%s"'%(y.company_name, y.company_name)+'},'
    return '['+cchoices+']'