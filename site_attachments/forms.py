__author__ = 'marc'
from django.forms import ModelForm
from commissioned_sites.models import SiteAttachment
from django.forms import TextInput

class SiteAttachmentForm(ModelForm):
    class Meta:
        model = SiteAttachment
        fields = ['file','site']


        widgets = {
            'site': TextInput(attrs={'type':'hidden'}),
        }
