__author__ = 'marc'
from django.forms import ModelForm
from parts.models import Part
from django import forms

class PartForm(ModelForm):
    class Meta:
        model = Part
        fields = ['description', 'model_number', 'note', 'official_model_name', 'part_number', 'end_of_life']

class ItemsMoveForm(forms.Form):
    destination_part = forms.IntegerField(widget = forms.Select(choices = [ ]), label='Move returned items to')

    def __init__(self, part, *args, **kwargs):
        # This should be done before any references to self.fields
        super(ItemsMoveForm, self).__init__(*args, **kwargs)

        # Change the field options
        parts = Part.objects.all()
        choices = []

        for p in parts:
            if p.id != part.id:
                choices.append((p.id, "%s-%s"%(p.description, p.model_number)))
        self.fields['destination_part'].widget.choices = choices