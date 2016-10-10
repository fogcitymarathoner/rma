
from django.http import HttpResponse
from django.conf import settings

from django.views.generic.edit import UpdateView
from django.views.generic.edit import CreateView
from django.views.generic import DeleteView

from django.contrib.auth.decorators import login_required

from commissioned_sites.models import SiteAttachment
from site_attachments.forms import SiteAttachmentForm

from django.core.urlresolvers import reverse
@login_required
def download_file(request, id):
    """
    Send a file through Django without loading the whole file into
    memory at once. The FileWrapper will turn the file object into an
    iterator for chunks of 8KB.
    """
    attach = SiteAttachment.objects.get(pk=id)

    filename = settings.COMMISSIONED_SITES_ATTACHMENTS_DIR+attach.file.name.encode('ascii','ignore')[1:] # Select your file here.


    #wrapper = FileWrapper(file(filename))
    #response = HttpResponse(wrapper, content_type='text/plain')
    #response['Content-Length'] = os.path.getsize(filename)

    file = open(filename, 'rb')
    content = file.read()
    file.close
    response = HttpResponse(content, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=%s'%filename

    return response




class SiteAttachmentsCreateView(CreateView):
    template_name = 'commissioned_sites/create_attachment.html'
    model = SiteAttachment
    fields = ['date']
    form_class = SiteAttachmentForm

    def get_success_url(self):
        return (reverse('site_manage_attachments', kwargs={'id': self.object.site.id}))

    def get_initial(self):
        site = Site.objects.get(pk=self.kwargs['id'])
        return { 'site': site }
    def get_context_data(self, **kwargs):
        context = super(SiteAttachmentsCreateView, self).get_context_data(**kwargs)
        context['rma'] = Site.objects.get(pk=self.kwargs['id'])
        return context


class SiteAttachmentsDeleteView(DeleteView):
    model = SiteAttachment
    def get_object(self, queryset=None):
        obj = SiteAttachment.objects.get(id=self.kwargs['id'])
        return obj
    def get_success_url(self):
        return (reverse('site_manage_attachments', kwargs={'id': self.object.site.id}))