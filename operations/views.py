import redis
import json
import re
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate
from parts.forms import ItemsMoveForm
from return_merchandise_authorizations.models import Rma
from return_merchandise_authorizations.models import Item
from parts.models import Part
from customers.models import CustomerCompany
from customers.forms import CustomerForm
from customers.forms import CustomerSiteIdNameForm
from operations.forms import CustomerCompanyAndSiteNameForm
from operations.forms import change_password_form
from return_merchandise_authorizations.lib import site_autocomplete_dropdown_selections
from return_merchandise_authorizations.acl import user_role
from return_merchandise_authorizations.acl import admin_role_required
from customers.models import Customer

from return_merchandise_authorizations.acl import user_role_required
@login_required
def reassign_customers_to_customer_sites(request):
    """
    show list of sites belonging to unknown company
    :param request:
    :return:
    """
    sites = Customer.objects.filter(customer__company_name = 'UNKNOWNCOMPANY').order_by('name')
    return render(request, 'operations/sites_index.html',
                  {'sites': sites},
        context_instance=RequestContext(request))

@login_required
def admin_rma_extra_fields(request):
    r = redis.StrictRedis(host='localhost', port=6379, db=settings.SESSION_REDIS_DB)
    message = ''
    if request.method == 'GET':
        rfields = json.loads(r.get(settings.SUB_URL.replace('/','')+':rma_extra_data'))
        #rfields = ['a', 'b']
        fields = []
        i = 0
        for f in rfields:
            obj = {
                'key': 'key_'+str(i),
                'value': f
            }
            i += 1
            fields.append(obj)
    if request.method == 'POST':
        #
        # Save to Redis
        #
        if request.POST['new_field'] == 'yes':
            # new empty field requested
            #
            # put keys in sortable-on-order dictionary
            rfields = []
            for k in request.POST.keys():
                if re.search('^key_', k) and request.POST[k] != '':
                    rfields.append({
                        'value': request.POST[k]
                    })
            rfields_sorted = sorted(rfields, key=lambda k: k['value'])
            fields = []
            i = 0
            for f in rfields_sorted:
                obj = {
                    'key': 'key_'+str(i),
                    'value': f['value']
                }
                i += 1
                fields.append(obj)
            fields.append({
                'key': 'key_'+str(i),
                'value': ''
            })

        else:
            # save and return with save message.

            fields = []
            rfields = []
            i = 0
            for k in request.POST.keys():
                if re.search('^key_', k) and request.POST[k] != '':
                    rfields.append(request.POST[k])
                    obj = {
                        'key': 'key_'+str(i),
                        'value': request.POST[k]
                    }
                    i += 1
                    fields.append(obj)

            r.set(settings.SUB_URL.replace('/','')+':rma_extra_data', json.dumps(sorted(rfields)))
            message = 'Field Names Saved'
    return render(request, 'operations/admin_rma_extra_fields.html',
                  {'fields': fields,
                   'message': message
                  },
        context_instance=RequestContext(request))

@login_required
def move_parts(request):
    parts = Part.objects.all()
    parts_count = []
    for p in parts:
        mod_part = {
            'id': p.id,
            'description': p.description,
            'model_number': p.model_number,
            'count': len(Item.objects.filter(part=p))
        }
        parts_count.append(mod_part)
    return render(request, 'operations/parts_index.html',
                  {'parts': parts_count},
        context_instance=RequestContext(request))

@login_required
def assign_customer_to_site_new_customer(request, id):

    if request.method == 'GET':
        site = Customer.objects.get(pk=id)
        site_rmas = Rma.objects.filter(customer=site)
        customer_name_form = CustomerForm()
        site_form = CustomerSiteIdNameForm(instance=site)
        return render(request, 'operations/edit_site_new_customer.html',
                  {
                      'site': site,
                      'customer_name_form': customer_name_form,
                      'site_form': site_form,
                      'site_rmas': site_rmas
                  },
        context_instance=RequestContext(request))

    if request.method == 'POST':
        site = Customer.objects.get(pk=id)
        error_count = 0
        customer_name_form = CustomerForm(request.POST)
        site_form = CustomerSiteIdNameForm(request.POST, instance=site)
        site_rmas = Rma.objects.filter(customer=site)
        if site_form.is_valid() is not True:
            error_count += 1
        if customer_name_form.is_valid() is not True:
            error_count += 1

        if error_count > 0:
            return render(request, 'operations/edit_site_new_customer.html',
                {
                      'site': site,
                      'customer_name_form': customer_name_form,
                      'site_form': site_form,
                      'site_rmas': site_rmas,
                },
                context_instance=RequestContext(request))
        else:
            new_customer = customer_name_form.save()
            new_customer_site = Customer()
            new_customer_site.name = site_form.cleaned_data['name']
            new_customer_site.customer = new_customer
            new_customer_site.save()

            return HttpResponseRedirect(reverse('view_customer_site_to_reassign', kwargs={'id': new_customer_site.id}))
@login_required
def view_part_to_move(request, id):
    if request.user.groups.filter(name='user').exists() is False:
            return render(request, 'errors/operation_not_allowed.html',
                  {},
        context_instance=RequestContext(request))
    else:
        part = Part.objects.get(pk=id)
        items = Item.objects.filter(part=id)
        return render(request, 'operations/view_part_to_move.html',
                      { 'part': part,
                        'items': items,
                        'item_count': len(items),
                        'form': ItemsMoveForm(part)
                      },
            context_instance=RequestContext(request))

@login_required
def view_customer_site_to_reassign(request, id):
    site = Customer.objects.get(pk=id)
    site_rmas = Rma.objects.filter(customer=site)
    return render(request, 'operations/view_site_to_reassign.html',
                  {
                      'site': site,
                      'site_rmas': site_rmas,
                  },
        context_instance=RequestContext(request))

@login_required
def assign_customer_select_customer(request, id):
    """
    Have user decide if site exists from list and reassign all rma to selected site and delete site
    :param request:
    :param id:
    :return:
    """
    site = Customer.objects.get(pk=id)
    site_rmas = Rma.objects.filter(customer=site)
    if request.method == 'GET':
        data = {
            'name': site_rmas[0].customer.name,
        }
        customer_name_site_form = CustomerCompanyAndSiteNameForm(initial=data)
        return render(request, 'operations/assign_customer_select_customer.html',
                  {
                      'site': site,
                      'form': customer_name_site_form,
                      'site_rmas': site_rmas
                  },
        context_instance=RequestContext(request))
    if request.method == 'POST':
        customer_name_site_form = CustomerCompanyAndSiteNameForm(request.POST)
        if customer_name_site_form.is_valid():

            new_site_name = customer_name_site_form.cleaned_data['name']
            existing_customer_id = int(customer_name_site_form.cleaned_data['customer'])
            existing_customer = CustomerCompany.objects.get(pk=existing_customer_id)
            new_site = Customer()
            new_site.customer = existing_customer
            new_site.name = new_site_name
            new_site.save()
            for s in site_rmas:
                s.customer = new_site
                s.save()
            site.delete()

            return HttpResponseRedirect(reverse('reassign_customers_to_customer_sites'))
        else:
            return render(request, 'operations/assign_customer_select_customer.html',
                      {
                          'site': site,
                          'form': customer_name_site_form,
                          'site_rmas': site_rmas
                      },
            context_instance=RequestContext(request))

@login_required
@user_role_required
def check_if_site_exists_and_reassign(request, id):
    """
    Have user decide if site exists from list and reassign all rma to selected site and delete site
    :param request:
    :param id:
    :return:
    """
    site = Customer.objects.get(pk=id)
    site_rmas = Rma.objects.filter(customer=site)
    if request.method == 'GET':
        return render(request, 'operations/edit_site.html',
                      {
                        'sites': site_autocomplete_dropdown_selections(),
                        'site': site,
                        'site_rmas': site_rmas,
                      },
            context_instance=RequestContext(request))

    if request.method == 'POST':
        # move rmas from old site to newly selected
        new_site = Customer.objects.get(pk=int(request.POST['customer']))
        for s in site_rmas:
            s.customer = new_site
            s.save()
        site.delete()
        return HttpResponseRedirect(reverse('reassign_customers_to_customer_sites'))
@login_required
@admin_role_required
def manage_users_roles(request):
    users = User.objects.all().order_by('username')
    users_roles = []
    for u in users:
        if u.is_active:
                users_roles.append({'user': u, 'role': user_role(u)})
    context = {
        'users_roles': users_roles
    }
    return render(request, 'operations/manage_users_roles.html',
                  context,
        context_instance=RequestContext(request))

@login_required
@admin_role_required
def manage_user_roles(request, id):
    user = User.objects.get(pk=id)
    context = {
        'user': user,
        'role': user_role(user),
    }
    return render(request, 'operations/manage_user_roles.html',
                  context,
        context_instance=RequestContext(request))


@login_required
def change_password(request):
    if request.method == 'POST':
        form = change_password_form(request.POST)
        if form.is_valid():
            newpassword=form.cleaned_data['newpassword1']
            request.user.set_password(newpassword)
            request.user.save()
            return render(request, 'errors/password_successfully_changed.html',
                  {},
                    context_instance=RequestContext(request))

        else:
           return render(request, 'operations/change_password.html',{'error':'You have entered bad data','form': form})
    else:
        form = change_password_form()
    return render(request, 'operations/change_password.html',
                  {'form': form},
        context_instance=RequestContext(request))