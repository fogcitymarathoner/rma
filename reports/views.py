from django.shortcuts import render

from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from reports.forms import PartsForm
from reports.forms import PartsAllTimeForm
from reports.forms import PartsNumbersForm
from reports.forms import CustomersForm
from reports.forms import YearQtrForm
from customers.models import CustomerCompany
from customers.models import Customer
from return_merchandise_authorizations.models import Rma
from return_merchandise_authorizations.models import Item
from return_merchandise_authorizations.settings import No
from return_merchandise_authorizations.settings import Yes
from parts.models import Part
from garage.logger import logger
from return_merchandise_authorizations.views import view_dict
from return_merchandise_authorizations.acl import user_role
@login_required
def parts(request):
    """
    Show the parts report generator
    :param request:
    :return:
    """
    return render(request, 'reports/parts.html',
                  {
                      'form': PartsForm(),
                  },
        context_instance=RequestContext(request))

@login_required
def parts_all_time(request):
    return render(request, 'reports/parts_all_time.html',
                  {
                      'form': PartsAllTimeForm(),
                  },
        context_instance=RequestContext(request))
@login_required
def parts_by_part_number(request):
    return render(request, 'reports/parts_by_part_number.html',
                  {
                      'form': PartsNumbersForm(),
                  },
        context_instance=RequestContext(request))


@login_required
def parts_by_quarter_by_site(request):
    return render(request, 'reports/parts_by_quarter_by_site.html',
                  {
                      'form': YearQtrForm(),
                  },
        context_instance=RequestContext(request))

@login_required
def report_parts_in_life(request):
    return render(request, 'reports/report_parts_in_out_of_life.html',
                  {
                      'parts': Part.objects.filter(end_of_life=No),
                      'in_life': True,
                  },
        context_instance=RequestContext(request))
@login_required
def report_parts_out_of_life(request):
    return render(request, 'reports/report_parts_in_out_of_life.html',
                  {
                      'parts': Part.objects.filter(end_of_life=Yes),
                      'in_life': False,
                  },
        context_instance=RequestContext(request))
@login_required
def unapproved_rmas(request):
    """
    Show the parts report generator
    :param request:
    :return:
    """
    return render(request, 'reports/unapproved_rmas.html',
                  {
                      'unapproved_rmas': Rma.objects.filter(approved=No),
                  },
        context_instance=RequestContext(request))

@login_required
def report_return_inventory(request):
    return render(request, 'reports/returns_against_inventory.html',
                  {
                      'su_cable_count': len(Item.objects.filter(part__description__startswith='SU Cable')),
                      'sensor_unit_count': len(Item.objects.filter(part__description__startswith='Sensor Unit')),
                      'other_count': len(Item.objects.filter(part__description__startswith='Other')),
                      'led_tube_light_count': len(Item.objects.filter(part__description__startswith='LED Tube Light')),
                      'led_driver_count': len(Item.objects.filter(part__description__startswith='LED Driver')),
                      'gateway_count': len(Item.objects.filter(part__description__startswith='Gateway')),
                      'energy_manager_count': len(Item.objects.filter(part__description__startswith='Energy Manager')),
                      'control_unit_count': len(Item.objects.filter(part__description__startswith='Control Unit')),
                      'ballast_count': len(Item.objects.filter(part__description__startswith='Ballast')),
                  },
        context_instance=RequestContext(request))

@login_required
def report_customer_rma(request):
    return render(request, 'reports/customers_rma.html',
                  {
                      'form': CustomersForm(),
                  },
        context_instance=RequestContext(request))

@login_required
def report_customer_sites(request):
    customers = CustomerCompany.objects.all().order_by('company_name')
    i = 0
    for c in customers:
        sites = Customer.objects.filter(customer=c).order_by('name')
        customers[i].sites = sites
        i += 1
    return render(request, 'reports/customers_sites.html',
                  {
                      'customers': customers,
                  },
        context_instance=RequestContext(request))


@login_required
def show_sites_rmas(request, id):
    return render(request, 'reports/view_site_rmas.html',
                    {
                        'customer': Customer.objects.get(pk=id),
                        'rmas': Rma.objects.filter(customer_id=id)
                    },
        context_instance=RequestContext(request))


@login_required
def show_rma(request, id):

    return render(request, 'reports/view_rma.html',
                  view_dict(id),
        context_instance=RequestContext(request))

@login_required
def report_user_roles(request):
    users = User.objects.all().order_by('username')
    users_roles = []
    for u in users:
        if u.is_active:
                users_roles.append({'user': u, 'role': user_role(u)})
    context = {
        'users_roles': users_roles
    }
    return render(request, 'reports/user_roles.html',
                  context,
        context_instance=RequestContext(request))


def operation_not_allowed(request):
    """
    display operation not allowed page after redirection from user_role_required decorator
    :param request:
    :return:
    """
    return render(request, 'errors/operation_not_allowed.html',
                  {
                      'form': PartsForm(),
                  },
        context_instance=RequestContext(request))
