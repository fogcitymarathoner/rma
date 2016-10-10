__author__ = 'marc'
from django.forms import ModelForm
from return_merchandise_authorizations.models import RmaAttachment
from commissioned_sites.models import SiteAttachment
from django.forms import TextInput
class RmaAttachmentForm(ModelForm):
    class Meta:
        model = RmaAttachment
        fields = ['file','rma']


        widgets = {
            'rma': TextInput(attrs={'type':'hidden'}),
        }

class SiteAttachmentForm(ModelForm):
    class Meta:
        model = SiteAttachment
        fields = ['file','site']


        widgets = {
            'site': TextInput(attrs={'type':'hidden'}),
        }
