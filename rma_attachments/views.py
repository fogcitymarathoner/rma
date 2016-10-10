from return_merchandise_authorizations.models import RmaAttachment
from commissioned_sites.models import SiteAttachment
from return_merchandise_authorizations.models import Rma
from django.views.generic.edit import DeleteView
from django.views.generic.edit import CreateView
from rma_attachments.forms import RmaAttachmentForm
from rma_attachments.forms import SiteAttachmentForm

from django.core.urlresolvers import reverse

class RmaAttachmentsCreateView(CreateView):
    template_name = 'rma_attachments/create.html'
    model = RmaAttachment
    fields = ['date']
    form_class = RmaAttachmentForm

    def get_success_url(self):
        return (reverse('manage_attachments', kwargs={'id': self.object.rma.id}))

    def get_initial(self):
        rma = Rma.objects.get(pk=self.kwargs['id'])
        return { 'rma': rma }
    def get_context_data(self, **kwargs):
        context = super(RmaAttachmentsCreateView, self).get_context_data(**kwargs)
        context['rma'] = Rma.objects.get(pk=self.kwargs['id'])
        return context


class RmaAttachmentsDeleteView(DeleteView):
    model = RmaAttachment
    def get_object(self, queryset=None):
        obj = RmaAttachment.objects.get(id=self.kwargs['id'])
        return obj
    def get_success_url(self):
        return (reverse('manage_attachments', kwargs={'id': self.object.rma.id}))


class SiteAttachmentsCreateView(CreateView):
    template_name = 'commissioned_sites/create_attachment.html'
    model = SiteAttachment
    fields = ['date']
    form_class = SiteAttachmentForm

    def get_success_url(self):
        return (reverse('site_manage_attachments', kwargs={'id': self.object.rma.id}))

    def get_initial(self):
        site = Site.objects.get(pk=self.kwargs['id'])
        return { 'site': site }
    def get_context_data(self, **kwargs):
        context = super(SiteAttachmentsCreateView, self).get_context_data(**kwargs)
        context['rma'] = Rma.objects.get(pk=self.kwargs['id'])
        return context


class SiteAttachmentsDeleteView(DeleteView):
    model = RmaAttachment
    def get_object(self, queryset=None):
        obj = RmaAttachment.objects.get(id=self.kwargs['id'])
        return obj
    def get_success_url(self):
        return (reverse('site_manage_attachments', kwargs={'id': self.object.rma.id}))