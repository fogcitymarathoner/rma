from django.shortcuts import render

from return_merchandise_authorizations.models import Item

from operator import itemgetter
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.views.generic.edit import UpdateView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from returned_items.forms import ItemForm
from returned_items.forms import ItemFormWithRMA
from return_merchandise_authorizations.models import Rma
from parts.models import Part
import re

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import Group
@login_required
def index(request):
    items = Item.objects.all()
    items_dated = []
    for i in items:
        obj = {
            'id': i.id,
            'note': i.note,
            'quantity': i.quantity,
            'date': i.rma.date,
            'rma_id': i.rma.id,
            'part_description': i.part.description,
            'part_model_number': i.part.model_number,
            'issue': i.rma.issue
        }
        items_dated.append(obj)
    items_sorted = sorted(items_dated, key=itemgetter('date'), reverse=True)
    return render(request, 'returned_items/index.html',
                  {'items': items_sorted},
        context_instance=RequestContext(request))

@login_required
def move_items_confirm(request):
    """
    change a list of returned items parts
    :param request:
    :return:
    """
    pattern = '^part-'
    part = Part.objects.get(pk=request.POST['destination_part'])
    # loop through keys and values
    items = []
    for key, value in request.POST.iteritems():
        if re.match(pattern, key):
            items.append(Item.objects.get(pk=value))
    return render(request, 'returned_items/confirm_move.html',
                  {'items': items,
                    'dest_part': part,
                    'src_part': items[0].part,
                  },
        context_instance=RequestContext(request))
@login_required
def move_items(request):
    """
    called after confirming move change a list of returned items parts after confirmation
    :param request:
    :return:
    """
    pattern = '^part-'
    part = Part.objects.get(pk=request.POST['dest-part-id'])
    # loop through keys and values
    for key, value in request.POST.iteritems():
        if re.match(pattern, key):
            returned_item = Item.objects.get(pk=value)
            returned_item.part = part
            returned_item.save()
    return redirect(reverse('view_part_to_move', kwargs={'id': part.id}))
class ReturnedItemCreateView(CreateView):
    template_name = 'returned_items/create.html'
    model = Item
    fields = ['date']
    form_class = ItemForm

    def get_success_url(self):
        return (reverse('manage_items', kwargs={'id': self.object.rma.id}))
    # ...
    def get_initial(self):
        rma = Rma.objects.get(pk=self.kwargs['id'])
        return { 'rma': rma }
    def get_context_data(self, **kwargs):
        context = super(ReturnedItemCreateView, self).get_context_data(**kwargs)
        context['rma'] = Rma.objects.get(pk=self.kwargs['id'])
        return context

    def post(self, request, **kwargs):
        form = ItemForm(request.POST)


        if form.is_valid():
            part_id = int(request.POST['part'])
            rma = Rma.objects.get(pk=self.kwargs['id'])
            part = Part.objects.get(pk=part_id)
            quantity = request.POST['quantity']
            note = request.POST['note']
            if rma is not None and part is not None and quantity > 0 and quantity is not None:
                item = Item()
                item.rma = rma
                item.part = part
                item.note = note
                item.quantity = quantity
                item.save()
                return redirect(reverse('manage_items', kwargs={'id': self.kwargs['id']}))
        else:
            self.object = Rma.objects.get(id=self.kwargs['id'])

            context = self.get_context_data(form=form)
            return self.render_to_response(context)

    def get(self, request, **kwargs):
        user_group = Group.objects.get(name='user')
        if request.user.groups.filter(name='user').exists() is False:
            return render(request, 'errors/cannot_create.html',
                  {},
        context_instance=RequestContext(request))
        else:
			self.object = Rma.objects.get(id=self.kwargs['id'])
			form_class = self.get_form_class()
			form = self.get_form(form_class)
			context = self.get_context_data(form=form)
			return self.render_to_response(context)
class ReturnedItemUpdateView(UpdateView):
    template_name = 'returned_items/edit.html'
    model = Item
    fields = ['date']
    form_class = ItemForm
    def get(self, request, **kwargs):
        user_group = Group.objects.get(name='user')
        if request.user.groups.filter(name='user').exists() is False:
            return render(request, 'errors/cannot_create.html',
                  {},
        context_instance=RequestContext(request))
        else:
            self.object = Item.objects.get(id=self.kwargs['id'])
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            context = self.get_context_data(object=self.object, form=form)
            return self.render_to_response(context)

    def get_object(self, queryset=None):
        obj = Item.objects.get(id=self.kwargs['id'])
        return obj

    def get_success_url(self):
        return (reverse('manage_items', kwargs={'id': self.object.rma.id}))

    def get_context_data(self, **kwargs):
        context = super(ReturnedItemUpdateView, self).get_context_data(**kwargs)
        ritem = self.get_object()
        context['rma'] = Rma.objects.get(pk=ritem.rma_id)
        return context
class ReturnedItemDeleteView(DeleteView):
    model = Item
    def get_object(self, queryset=None):
        obj = Item.objects.get(id=self.kwargs['id'])
        return obj
    def get_success_url(self):
        return (reverse('manage_items', kwargs={'id': self.object.rma.id}))


    def get(self, request, **kwargs):
        user_group = Group.objects.get(name='user')
        if request.user.groups.filter(name='user').exists() is False:
            return render(request, 'errors/cannot_delete.html',
                  {},
        context_instance=RequestContext(request))
        else:

            return render(request, 'return_merchandise_authorizations/item_confirm_delete.html',
                  {'object': self.get_object()},
        context_instance=RequestContext(request))