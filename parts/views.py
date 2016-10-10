from django.shortcuts import render

from parts.models import Part
from parts.forms import PartForm
from return_merchandise_authorizations.models import Item
from django.views.generic.edit import UpdateView
from django.views.generic.edit import CreateView
from django.views.generic import DeleteView
from django.template import RequestContext
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import Group
@login_required
def index(request):
    parts = Part.objects.all()
    parts_count = []
    for p in parts:
        mod_part = {
            'id': p.id,
            'description': p.description,
            'model_number': p.model_number,
            'official_model_name': p.official_model_name,
            'part_number': p.part_number,
            'count': len(Item.objects.filter(part=p))
        }
        parts_count.append(mod_part)
    return render(request, 'parts/index.html',
                  {'parts': parts_count},
        context_instance=RequestContext(request))

@login_required
def view(request, id):
    part = Part.objects.get(pk=id)
    items = Item.objects.filter(part=id)
    return render(request, 'parts/view.html',
                  { 'part': part,
                    'items': items,
                    'item_count': len(items),
                  },
        context_instance=RequestContext(request))


class PartCreateView(CreateView):
    template_name = 'parts/create.html'
    model = Part
    fields = ['description']
    form_class = PartForm
class PartUpdateView(UpdateView):
    template_name = 'parts/edit.html'
    model = Part
    fields = ['date']
    form_class = PartForm
    def get(self, request, **kwargs):
        self.object = Part.objects.get(id=self.kwargs['id'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        obj = Part.objects.get(id=self.kwargs['id'])
        return obj
class PartUpdateOpsView(UpdateView):
    template_name = 'parts/edit.html'
    model = Part
    fields = ['date']
    form_class = PartForm
    def get(self, request, **kwargs):
        self.object = Part.objects.get(id=self.kwargs['id'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        obj = Part.objects.get(id=self.kwargs['id'])
        return obj

    def get_success_url(self):
        obj = self.get_object()
        return (reverse('view_part_to_move', args=(), kwargs={'id': obj.id}))

class PartDeleteView(DeleteView):
    model = Part
    def get_object(self, queryset=None):
        obj = Part.objects.get(id=self.kwargs['id'])
        return obj
    def get_success_url(self):
        return (reverse('list_parts'))


    def get(self, request, **kwargs):
        user_group = Group.objects.get(name='user')
        if request.user.groups.filter(name='user').exists() is False:
            return render(request, 'errors/cannot_delete.html',
                  {},
        context_instance=RequestContext(request))
        else:

            return render(request, 'parts/part_confirm_delete.html',
                  {'object': self.get_object()},
        context_instance=RequestContext(request))
class PartDeleteOpsView(DeleteView):
    model = Part
    def get_object(self, queryset=None):
        obj = Part.objects.get(id=self.kwargs['id'])
        return obj
    def get_success_url(self):
        return (reverse('move_parts'))

    def get(self, request, **kwargs):
        user_group = Group.objects.get(name='user')
        if request.user.groups.filter(name='user').exists() is False:
            return render(request, 'errors/cannot_delete.html',
                  {},
        context_instance=RequestContext(request))
        else:

            return render(request, 'parts/part_ops_confirm_delete.html',
                  {'object': self.get_object()},
        context_instance=RequestContext(request))