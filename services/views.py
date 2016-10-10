from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from return_merchandise_authorizations.models import Item
from parts.models import Part
from customers.models import Customer
from return_merchandise_authorizations.models import Rma
from returned_items.forms import ItemForm

from django.template import RequestContext
from datetime import datetime as dt
from services.lib import quarter_query_range
from services.lib import quarter_to_str
from return_merchandise_authorizations.acl import assign_admin
from return_merchandise_authorizations.acl import assign_poweruser
from return_merchandise_authorizations.acl import assign_approver
from return_merchandise_authorizations.acl import assign_user
from return_merchandise_authorizations.acl import assign_viewer
from return_merchandise_authorizations.acl import admin_role_required
from return_merchandise_authorizations.acl import user_role_required
@login_required
def returned_parts_by_quarter_by_site(request, year, quarter):
    """

    :param request:
    :param number:
    :return:
    """
    # fixme - this can be written better with fewer calls to database
    #  collect lists of objects instead of primary keys
    #
    query_begin, query_end = quarter_query_range(year, quarter)
    qrparts = Item.objects.filter(rma__date__gte = query_begin).filter(rma__date__lte = query_end). \
                            order_by('rma__customer__name')
    qrparts_sort_on_description = Item.objects.filter(rma__date__gte = query_begin).filter(rma__date__lte = query_end). \
                            order_by('part__description')
    parts_unique = []
    parts_summary = []
    for i in qrparts_sort_on_description:
        if i.part.id not in parts_unique:
            parts_unique.append(i.part.id)
    print parts_unique
    for i in parts_unique:
        print i
        returns = Item.objects.filter(part__id=i).filter(rma__date__gte = query_begin).filter(rma__date__lte = query_end)
        count = 0
        for k in returns:
            count += k.quantity
        print returns
        print count
        o = {
            'part': Part.objects.get(pk=i),
            'count': count,
        }
        parts_summary.append(o)
    sites = []
    for p in qrparts:
        if p.rma.customer.id not in sites:
            sites.append(p.rma.customer.id)

    site_parts = []
    for s in sites:
        parts = Item.objects.filter(rma__customer_id = s).filter(rma__date__gte = query_begin).filter(rma__date__lte = query_end)
        parts_list = []
        parts_list_counts = []
        for p in parts:
            if p.part.id not in parts_list:
                parts_list.append(p.part.id)
        for p in parts_list:
            customer_part_returns = Item.objects.filter(part__id=p).filter(rma__customer_id = s).filter(rma__date__gte = query_begin).filter(rma__date__lte = query_end)
            count = 0
            for n in customer_part_returns:
                count += n.quantity
            parts_list_counts.append( {
                'part': Part.objects.get(pk=p),
                'count': count,
            })
        site_parts.append({'site': Customer.objects.get(pk=s),
                           'parts': parts_list_counts,
        })

    return render(request, 'services/_returned_parts_by_quarter_by_site.html',
                  {
                      'year': year,
                      'quarter': quarter_to_str(quarter),
                      'site_parts': site_parts,
                      'summary': parts_summary,
                  },
        context_instance=RequestContext(request))
@login_required
def numbered_returned_item_form(request, number):
    """
    Return a return item form with the number given by jquery
    :param request:
    :param number:
    :return:
    """
    form = ItemForm().as_table().replace('quantity"', 'quantity_'+str(number)+'"').replace('part"', 'part_'+str(number)+'"').replace('note"', 'note_'+str(number)+'"'),

    return render(request, 'services/_customer_form.html',
                  {'form': form[0]},
        context_instance=RequestContext(request))

@login_required
def returned_part_in_period_report(request, part_number, start_year, start_month, start_day, end_year, end_month,
                                   end_day):
    items = Item.objects.filter(part_id=part_number). \
                        filter(rma__date__gte=dt.strptime(start_year+'-'+start_month+'-'+start_day, '%Y-%b-%d')). \
                        filter(rma__date__lte=dt.strptime(end_year+'-'+end_month+'-'+end_day, '%Y-%b-%d'))


    return render(request, 'services/_parts_report.html',
                  {'items': items},
        context_instance=RequestContext(request))

@login_required
def returned_part_all_time_report(request, part_number):
    items = Item.objects.filter(part_id=part_number)
    return render(request, 'services/_parts_report.html',
                  {'items': items},
        context_instance=RequestContext(request))

@login_required
def returned_part_by_part_number_report(request, part_number):
    items = Item.objects.filter(part__part_number=part_number)

    return render(request, 'services/_parts_report.html',
                  {'items': items},
        context_instance=RequestContext(request))

@login_required
@user_role_required
def customers_sites_dropdown(request, number):
    return render(request, 'customers/_customer_sites_dropdown.html',
                  {
                        'sites': Customer.objects.filter(customer_id=number)
                  },
        context_instance=RequestContext(request))
@login_required
def customers_rmas_report(request, number):
    """
    Return a return item form with the number given by jquery
    :param request:
    :param number:
    :return:
    """
    return render(request, 'customers/_view_rmas.html',
                  {
                        'rmas': Rma.objects.filter(customer_id=number)
                  },
        context_instance=RequestContext(request))

@login_required
@admin_role_required
def assign_role(request, id, role):
    user = User.objects.get(pk=id)
    if role == 'admin':
        assign_admin(user)
    if role == 'poweruser':
        assign_poweruser(user)
    if role == 'approver':
        assign_approver(user)
    if role == 'user':
        assign_user(user)
    if role == 'viewer':
        assign_viewer(user)
    return render(request, 'services/_user_role_reassigned.html',
                  {
                        'user': User.objects.get(pk=id),
                        'role': role,
                  },
        context_instance=RequestContext(request))