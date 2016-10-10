__author__ = 'marc'
from django.forms import ModelForm
from django.forms import TextInput
from django.forms import HiddenInput
from django import forms
from return_merchandise_authorizations.models import Rma
from return_merchandise_authorizations.settings import SHIPPING_CHOICES
from datetime import datetime as dt
"""
RmaForm is a RMA for existing customers
TroubleTicket is an RMA creating a new customer.
"""
# Create the form class.
class RmaForm(ModelForm):

    shipping = forms.ChoiceField(choices=SHIPPING_CHOICES)
    last_modified_on = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = Rma
        fields = ['customer', 'date', 'case_number', 'reference_number', 'contact', 'contact_phone_number', 'address',
               'issue', 'shipping', 'outbound_tracking_number',
               'return_tracking_number', 'root_cause_analysis', 'phase', 'repair_costs', 'last_modified_by', 'last_modified_on']

        widgets = {
            'reference_number': TextInput(attrs={'readonly':'readonly'}),
            'customer': TextInput(attrs={'readonly':'readonly'}),
        }
    def __init__(self, *args, **kwargs):
        # This should be done before any references to self.fields
        super(RmaForm, self).__init__(*args, **kwargs)

        self.fields['date'].initial = dt.now().strftime('%Y-%m-%d')
        self.fields['contact'].label = 'Contact*:'
        self.fields['case_number'].label = 'Case Number*:'
        self.fields.keyOrder = [
            'customer', 'date', 'case_number', 'reference_number', 'contact', 'contact_phone_number', 'address',
                'issue', 'shipping', 'outbound_tracking_number',
               'return_tracking_number', 'root_cause_analysis', 'phase', 'repair_costs', 'last_modified_by', 'last_modified_on']


class RmaTroubleTicketForm(ModelForm):
    shipping = forms.ChoiceField(choices=SHIPPING_CHOICES)
    class Meta:
        model = Rma
        fields = ['date', 'case_number', 'reference_number', 'contact', 'contact_phone_number', 'address',
                'issue', 'shipping', 'outbound_tracking_number',
               'return_tracking_number', 'root_cause_analysis', 'phase', 'repair_costs']

        widgets = {
            'reference_number': TextInput(attrs={'readonly':'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        # This should be done before any references to self.fields
        super(RmaTroubleTicketForm, self).__init__(*args, **kwargs)

        self.fields['date'].initial = dt.now().strftime('%Y-%m-%d')
        self.fields.keyOrder = [
            'customer', 'date', 'case_number', 'reference_number', 'contact', 'contact_phone_number', 'address',
                'issue', 'shipping', 'outbound_tracking_number',
               'return_tracking_number', 'root_cause_analysis', 'phase', 'repair_costs', 'last_modified_by', 'last_modified_on']
class RmaApprovalForm(ModelForm):
    class Meta:
        model = Rma
        fields = ['approved', 'approved_by', 'approved_on', 'approval_notes']

        widgets = {
            'approved_by': HiddenInput(attrs={'readonly':'readonly', 'hidden': 'True'}),
            'approved': HiddenInput(attrs={'readonly':'readonly', 'hidden': 'True'}),
        }
