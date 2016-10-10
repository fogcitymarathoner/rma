__author__ = 'marc'

from django import forms
from customers.models import Customer
from customers.models import CustomerCompany


class CustomerCompanyAndSiteNameForm(forms.Form):

    customer = forms.IntegerField(widget = forms.Select(choices = [ ]), label='Select Customer')
    name = forms.CharField(label='Site Name')
    def __init__(self, *args, **kwargs):
        # This should be done before any references to self.fields
        super(CustomerCompanyAndSiteNameForm, self).__init__(*args, **kwargs)
        companies = CustomerCompany.objects.exclude(company_name='UNKNOWNCOMPANY').order_by('company_name')

        cchoices = []
        for y in companies:
            cchoices.append((y.id, "%s"%(y.company_name)))

        self.fields['customer'].widget.choices = cchoices

class change_password_form(forms.Form):

    newpassword1 = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'type':'password', 'placeholder':'New Password',  'class' : 'span'}))
    newpassword2 = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'type':'password', 'placeholder':'Confirm New Password',  'class' : 'span'}))

    def clean(self):
        if 'newpassword1' in self.cleaned_data and 'newpassword2' in self.cleaned_data:
            if self.cleaned_data['newpassword1'] != self.cleaned_data['newpassword2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data