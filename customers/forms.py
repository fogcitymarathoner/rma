__author__ = 'marc'
from django import forms
from django.forms import TextInput
from customers.models import Customer
from customers.models import CustomerCompany
class CustomerForm(forms.ModelForm):

    class Meta:
        model = CustomerCompany
        fields = ['company_name']
        labels = {
            'company_name': 'Customer Name',
        }
class CustomerSiteNameEmptyDropdownForm(forms.ModelForm):

    name = forms.ModelChoiceField(queryset=Customer.objects.filter(customer__company_name='xxxx'), label= 'Site*:', empty_label="If you don't see your site for this customer exit and make a new site for this customer")
    class Meta:
        model = Customer
        fields = ['name']
class CustomerNameDropdownForm(forms.ModelForm):

    company_name = forms.ModelChoiceField(queryset=CustomerCompany.objects.all().order_by('company_name'), label= 'Customer Company', empty_label="If you don't see your customer exit and make a new site for this customer")
    class Meta:
        model = CustomerCompany
        fields = ['company_name']

class CustomerSiteIdNameForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name']
        labels = {
            'name': 'Customer Site Name',
        }
class CustomerSiteForm(forms.ModelForm):

    customer = forms.ModelChoiceField(queryset=CustomerCompany.objects.all().order_by('company_name'), label='Customer Name', empty_label="Please Select Customer")
    class Meta:
        model = Customer
        fields = ['customer', 'name']

        labels = {
            'name': 'Customer Site Name',
        }
