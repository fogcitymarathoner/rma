__author__ = 'marc'
from django import forms
from parts.models import Part
from return_merchandise_authorizations.models import Rma
from customers.models import Customer
from django import forms
from datetime import datetime as dt

from django.conf import settings
class PartsForm(forms.Form):
    now = dt.now()
    part = forms.IntegerField(widget = forms.Select(choices = [ ]), label='Select Part')
    start_date = forms.DateField(
        widget=forms.widgets.DateInput(format="%m/%d/%Y"), label='Select a Start Date', initial=dt(now.year, 1, 1).strftime('%m/%d/%Y'))
    end_date = forms.DateField(
        widget=forms.widgets.DateInput(format="%m/%d/%Y"), label='Select a End Date', initial=dt(now.year, 12, 31).strftime('%m/%d/%Y'))
    def __init__(self, *args, **kwargs):
        # This should be done before any references to self.fields
        super(PartsForm, self).__init__(*args, **kwargs)

        # Change the field options
        parts = Part.objects.all().order_by('description')
        choices = []

        for p in parts:
            choices.append((p.id, "%s:%s"%(p.description, p.model_number)))
        self.fields['part'].widget.choices = choices

class YearQtrForm(forms.Form):
    year = forms.IntegerField(widget = forms.Select(choices = [ ]), label='Select Year')
    quarter = forms.IntegerField(widget = forms.Select(choices = [ ]), label='Select Quarter')

    def __init__(self, *args, **kwargs):
        # This should be done before any references to self.fields
        super(YearQtrForm, self).__init__(*args, **kwargs)
        now = dt.now()
        ychoices = []
        for y in range(settings.EPOCH_YEAR, now.year + 1):
            ychoices.append((y, "%s"%(y)))
        qchoices = []

        qchoices.append((0, "1st"))
        qchoices.append((1, "2nd"))
        qchoices.append((2, "3rd"))
        qchoices.append((3, "4th"))
        self.fields['year'].widget.choices = ychoices
        self.fields['quarter'].widget.choices = qchoices



class PartsAllTimeForm(forms.Form):
    part = forms.IntegerField(widget = forms.Select(choices = [ ]))
    def __init__(self, *args, **kwargs):
        # This should be done before any references to self.fields
        super(PartsAllTimeForm, self).__init__(*args, **kwargs)

        # Change the field options
        parts = Part.objects.all().order_by('description')
        choices = []
        choices.append(('','Please select part to search for' ))
        for p in parts:
            choices.append((p.id, "%s:%s"%(p.description, p.model_number)))
        self.fields['part'].widget.choices = choices

class PartsNumbersForm(forms.Form):
    part = forms.IntegerField(widget = forms.Select(choices = [ ]), label='Select Part')
    def __init__(self, *args, **kwargs):
        # This should be done before any references to self.fields
        super(PartsNumbersForm, self).__init__(*args, **kwargs)

        # Change the field options
        parts = Part.objects.all().order_by('part_number')
        choices = []

        choices.append(('','Please select part to search for' ))
        for p in parts:
            if p.part_number != '':
                if p.part_number != None:
                    choices.append((p.id, "%s:%s:%s"%(p.description, p.model_number, p.part_number)))
        self.fields['part'].widget.choices = choices


class CustomersForm(forms.Form):
    customer = forms.IntegerField(widget = forms.Select(choices = [ ]), label='Select Customer Site')
    def __init__(self, *args, **kwargs):
        # This should be done before any references to self.fields
        super(CustomersForm, self).__init__(*args, **kwargs)

        # Change the field options
        customers = Customer.objects.all().order_by('customer__company_name')
        choices = [('','Please Select a Customer Site')]

        for p in customers:
            choices.append((p.id, "%s-%s (RMA Count: %s)"%(p.customer.company_name, p.name, len(Rma.objects.filter(customer=p)))))
        self.fields['customer'].widget.choices = choices

