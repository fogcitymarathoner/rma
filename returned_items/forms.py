__author__ = 'marc'
from django.forms import ModelForm
from django import forms
from return_merchandise_authorizations.models import Item
from parts.models import Part
from django.forms import Select
from django.forms import TextInput

def get_part_choices():
    parts = Part.objects.all()
    res = []
    for p in parts:
        res.append(['%s'%p.id, '%s: %s'%(p.description, p.model_number)])
    return res

class ItemForm(ModelForm):
    part = forms.ModelChoiceField(Part.objects.all())

    class Meta:
        model = Item
        fields = [ 'part', 'quantity', 'note']
        widgets = {
            'quantity': TextInput(attrs={'type':'number', 'min':0, 'max':99999}),
        }
class ItemFormWithRMA(ModelForm):
    """
    need this to do a save
    """
    part = forms.ModelChoiceField(queryset=Part.objects.all().order_by('description'))
    class Meta:
        model = Item
        fields = [ 'part', 'quantity', 'note', 'rma']

        widgets = {
            'quantity': TextInput(attrs={'type':'number', 'min':0, 'max':99999}),
        }

    def clean(self):
        super(ItemFormWithRMA, self).clean()
        cleaned_data = self.cleaned_data
        return cleaned_data