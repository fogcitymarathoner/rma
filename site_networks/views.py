from commissioned_sites.models import Network
from commissioned_sites.models import CommissionedSite
from commissioned_sites.forms import NetworkForm
from django.views.generic.edit import UpdateView
from django.views.generic.edit import CreateView
from django.views.generic import DeleteView


from django.core.urlresolvers import reverse

class NetworkCreateView(CreateView):
    template_name = 'commissioned_sites/network_create.html'
    model = Network
    fields = ['date']
    form_class = NetworkForm

    def get_success_url(self):
        return (reverse('site_manage_networks', kwargs={'id': self.object.site.id}))
    # ...
    def get_initial(self):
        site = CommissionedSite.objects.get(pk=self.kwargs['id'])
        return { 'site': site }
    def get_context_data(self, **kwargs):
        context = super(NetworkCreateView, self).get_context_data(**kwargs)
        context['site'] = CommissionedSite.objects.get(pk=self.kwargs['id'])
        return context
class NetworkUpdateView(UpdateView):
    template_name = 'commissioned_sites/network_edit.html'
    model = Network
    fields = ['date']
    form_class = NetworkForm
    def get(self, request, **kwargs):
        self.object = Network.objects.get(id=self.kwargs['id'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        obj = Network.objects.get(id=self.kwargs['id'])
        return obj

    def get_success_url(self):
        return (reverse('site_manage_networks', kwargs={'id': self.object.site.id}))

    def get_context_data(self, **kwargs):
        context = super(NetworkUpdateView, self).get_context_data(**kwargs)
        site_network = self.get_object()
        context['site'] = CommissionedSite.objects.get(pk=site_network.site_id)
        return context
class NetworkDeleteView(DeleteView):
    model = Network
    def get_object(self, queryset=None):
        obj = Network.objects.get(id=self.kwargs['id'])
        return obj
    def get_success_url(self):
        return (reverse('site_manage_networks', kwargs={'id': self.object.site.id}))