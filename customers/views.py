import sys
from django.shortcuts import render

from django.views.generic.edit import UpdateView
from django.views.generic.edit import CreateView
from django.views.generic import DeleteView
from django.contrib.auth.models import Group
from customers.forms import CustomerForm
from customers.forms import CustomerSiteForm
from customers.forms import CustomerSiteIdNameForm
from customers.forms import CustomerNameDropdownForm
from django.template import RequestContext
from customers.models import Customer
from customers.models import CustomerCompany
from return_merchandise_authorizations.models import Rma

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from django.http import HttpResponseRedirect
from return_merchandise_authorizations.acl import user_role_required
from return_merchandise_authorizations.acl import user_role_required_class_method
@login_required
def view(request, id):
    company = CustomerCompany.objects.get(pk=id)
    return render(request, 'customers/view.html',
                    {
                        'customer': company,
                        'rmas': Rma.objects.filter(customer__customer=company),
                        'sites': Customer.objects.filter(customer=company)
                    },
        context_instance=RequestContext(request))

@login_required
def view_site(request, id):
    """
    show all the sites for the requested customer
    :param request:
    :param id:
    :return:
    """
    return render(request, 'customers/view_site.html',
                    {
                        'customer': Customer.objects.get(pk=id),
                        'rmas': Rma.objects.filter(customer_id=id)
                    },
        context_instance=RequestContext(request))

@login_required
def index_customer_sites(request):

    return render(request, 'customers/index_sites.html',
                  {'customers': Customer.objects.all().order_by('customer__company_name')},
        context_instance=RequestContext(request))


@login_required
def index(request):

    return render(request, 'customers/index.html',
                  {'customers': CustomerCompany.objects.all().order_by('company_name')},
        context_instance=RequestContext(request))


class CustomerCreateView(CreateView):
    template_name = 'customers/create.html'
    model = CustomerCompany
    fields = ['description']
    form_class = CustomerForm
    def get_success_url(self):
        return (reverse('view_customer', kwargs={'id': self.object.id}))
    @user_role_required_class_method
    def post(self, request, *args, **kwargs):
        return super(CustomerCreateView, self).post(self, *args, **kwargs)
    @user_role_required_class_method
    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response({'form':form})
class CustomerUpdateView(UpdateView):
    template_name = 'customers/edit.html'
    model = CustomerCompany
    fields = ['date']
    form_class = CustomerForm

    @user_role_required_class_method
    def post(self, request, *args, **kwargs):
        return super(CustomerUpdateView, self).post(self, *args, **kwargs)
    @user_role_required_class_method
    def get(self, request, **kwargs):
        self.object = CustomerCompany.objects.get(id=self.kwargs['id'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form, site=self.object)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        obj = CustomerCompany.objects.get(id=self.kwargs['id'])
        return obj

    def get_success_url(self):
        return (reverse('view_customer', kwargs={'id': self.object.id}))


class CustomerDeleteView(DeleteView):
    model = CustomerCompany
    def get_object(self, queryset=None):
        obj = CustomerCompany.objects.get(id=self.kwargs['id'])
        return obj
    def get_success_url(self):
        return (reverse('list_customers'))


    @user_role_required_class_method
    def post(self, request, *args, **kwargs):
        return super(CustomerDeleteView, self).post(self, *args, **kwargs)
    @user_role_required_class_method
    def get(self, request, **kwargs):
        return render(request, 'customers/customer_confirm_delete.html',
                  {'object': self.get_object()},
        context_instance=RequestContext(request))


class CustomerSiteCreateCustomerView(CreateView):
    template_name = 'customers/create_site_customer.html'
    model = Customer
    fields = ['description']
    form_class = CustomerSiteForm
    def get_success_url(self):
        return (reverse('view_customer_site', kwargs={'id': self.object.id}))
    @user_role_required_class_method
    def post(self, request, *args, **kwargs):
        return super(CustomerSiteCreateCustomerView, self).post(self, *args, **kwargs)
    @user_role_required_class_method
    def get(self, request, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response({'form':form, 'customer_id': kwargs['customer_id']})
class CustomerSiteCreateView(CreateView):
    template_name = 'customers/create_site.html'
    model = Customer
    fields = ['description']
    form_class = CustomerSiteForm
    def get_success_url(self):
        return (reverse('view_customer_site', kwargs={'id': self.object.id}))
    @user_role_required_class_method
    def post(self, request, *args, **kwargs):
        return super(CustomerSiteCreateView, self).post(self, *args, **kwargs)
    @user_role_required_class_method
    def get(self, request, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response({'form':form})
class CustomerSiteUpdateView(UpdateView):
    template_name = 'customers/edit_site.html'
    model = Customer
    fields = ['date']
    form_class = CustomerSiteForm

    @user_role_required_class_method
    def post(self, request, *args, **kwargs):
        return super(CustomerSiteUpdateView, self).post(self, *args, **kwargs)
    @user_role_required_class_method
    def get(self, request, **kwargs):
        self.object = Customer.objects.get(id=self.kwargs['id'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form, site=self.object)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        obj = Customer.objects.get(id=self.kwargs['id'])
        return obj

    def get_success_url(self):
        return (reverse('view_customer_site', kwargs={'id': self.object.id}))


class CustomerSiteDeleteView(DeleteView):
    model = CustomerSiteForm
    def get_object(self, queryset=None):
        obj = Customer.objects.get(id=self.kwargs['id'])
        return obj
    def get_success_url(self):
        return (reverse('list_customer_sites'))


    def get(self, request, **kwargs):
        user_group = Group.objects.get(name='user')
        if request.user.groups.filter(name='user').exists() is False:
            return render(request, 'errors/cannot_delete.html',
                  {},
        context_instance=RequestContext(request))
        else:

            return render(request, 'customers/customercompany_confirm_delete.html',
                  {'object': self.get_object()},
        context_instance=RequestContext(request))