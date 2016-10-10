from datetime import datetime as dt
import re
import os
import json
import redis
from bs4 import BeautifulSoup as bs
from bson.objectid import ObjectId
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect
from django.views.generic.edit import UpdateView
from django.views.generic.edit import CreateView
from django.views.generic import DeleteView
from django.contrib.auth import authenticate, login
from django.utils.translation import LANGUAGE_SESSION_KEY
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.signals import user_logged_out
from customers.models import Customer
from customers.models import CustomerCompany
from customers.forms import CustomerSiteNameEmptyDropdownForm
from customers.forms import CustomerNameDropdownForm
from return_merchandise_authorizations.models import Rma
from return_merchandise_authorizations.models import Item
from return_merchandise_authorizations.forms import RmaForm
from return_merchandise_authorizations.forms import RmaApprovalForm
from return_merchandise_authorizations.models import RmaAttachment
from garage.logger import logger

from returned_items.forms import ItemForm
from returned_items.forms import ItemFormWithRMA
from django.core.exceptions import ObjectDoesNotExist
from return_merchandise_authorizations.lib import site_autocomplete_dropdown_selections
from return_merchandise_authorizations.lib import mail_new_rma_message
from return_merchandise_authorizations.lib import mail_approved_rma_message
from pymongo import MongoClient

from return_merchandise_authorizations.acl import user_role_required
from return_merchandise_authorizations.acl import user_role_required_class_method
"""
this is the home page and has to be open to allow authentication
"""
def index(request):
    return render_to_response('return_merchandise_authorizations/index.html',
                  {'rmas': Rma.objects.all().order_by('-date')},
        context_instance=RequestContext(request))
# not an action
def _sync_mongo_keys(id):
    """
    make sure rma has all the extra fields it's supposed to
    :param id:
    :return:
    """
    r = redis.StrictRedis(host='localhost', port=6379, db=settings.SESSION_REDIS_DB)
    rkey = settings.SUB_URL.replace('/','')+':rma_extra_data'
    # make sure extra data key is in redis DB
    if r.exists(rkey):
        rfields = json.loads(r.get(rkey))
    else:
        rfields = []
        r.set(rkey, json.dumps(rfields))

    client = MongoClient()
    db = client[settings.MONGO_DB]
    extra_data = db.extra_data

    rma_extra_data = extra_data.find_one({"rma_id": id})
    # initialize mongo data if None
    if rma_extra_data == None:
        rma_extra_data = {
            'rma_id': id,
        }
        for f in rfields:
            rma_extra_data[f['value']] = ''

        extra_data.insert(rma_extra_data)
    # add new fields that have been added since last save
    for f in rfields:
        if f not in rma_extra_data.keys():
            rma_extra_data[f['value']] = ''
    return rma_extra_data
# not an action
def view_dict(id, message=None):

    rma_extra_data = _sync_mongo_keys(id)
    rma = Rma.objects.get(id=id)

    if rma.shipping == '1':
        rma.shipping = 'Fed Ex First Overnight'
    elif rma.shipping == '2':
        rma.shipping = 'Fed Ex Std Overnight'
    elif rma.shipping == '3':
        rma.shipping = 'Fed Ex 2Day'
    elif rma.shipping == '4':
        rma.shipping = 'Fed Ex Express Saver (3 Day)'
    items = Item.objects.filter(rma=rma)
    readable_items = []
    for i in items:
        new_i = {
            'name': i.part.description,
            'id': i.id,
            'quantity': i.quantity,
            'model_number': i.part.model_number
        }
        readable_items.append(new_i)

    attachs = RmaAttachment.objects.filter(rma=rma)
    attachments = []
    for i in attachs:
        new_i = {
            'file': i.file,
            'id': i.id,
        }
        attachments.append(new_i)
    return {'rma': rma,
           'items': readable_items,
           'attachments': attachments,
           'rma_extra_data': rma_extra_data,
           'message': message
          }


@login_required
@user_role_required
def create(request):

    if request.method == 'GET':
        data = {
            'last_modified_by': request.user,
            'last_modified_on': dt.now(),
        }
        form = RmaForm(initial=data)
        customer_form = CustomerSiteNameEmptyDropdownForm()
        items = [ItemForm().as_table().replace('quantity"', 'quantity_'+str(0)+'"').replace('part"', 'part_'+str(0)+'"').replace('note"', 'note_'+str(0)+'"'),
                 ItemForm().as_table().replace('quantity"', 'quantity_'+str(1)+'"').replace('part"', 'part_'+str(1)+'"').replace('note"', 'note_'+str(1)+'"'),
                 ItemForm().as_table().replace('quantity"', 'quantity_'+str(2)+'"').replace('part"', 'part_'+str(2)+'"').replace('note"', 'note_'+str(2)+'"')]
        return render(request, 'return_merchandise_authorizations/create.html',
            {
                'form':form,
                'customer_form': customer_form,
                'items':items,
            },
            context_instance=RequestContext(request))


    if request.method == 'POST':

        error_count = 0
        item_mesg = ''

        data = {
            "customer": request.POST['name'],
            'date': request.POST['date'],
            'case_number':  request.POST['case_number'],
            'reference_number':  request.POST['reference_number'],
            'contact':  request.POST['contact'],
            'contact_phone_number':  request.POST['contact_phone_number'],
            'address':  request.POST['address'],
            'issue':  request.POST['issue'],
            'shipping':  request.POST['shipping'],
            'outbound_tracking_number':  request.POST['outbound_tracking_number'],
            'return_tracking_number':  request.POST['return_tracking_number'],
            'root_cause_analysis':  request.POST['root_cause_analysis'],
            'phase':  request.POST['phase'],
            'repair_costs':  request.POST['repair_costs'],
            'last_modified_by':  request.user.id,
            'last_modified_on':  dt.now().strftime('%Y-%m-%d'),
        }
        rma_form = RmaForm(data)
        customer_form = CustomerSiteNameEmptyDropdownForm()
        """
        gather parts into 3 arrays parts, part_notes, and part_quantities
        """
        parts = []
        part_notes = []
        part_quantities = []
        for k in request.POST.keys():
            if re.search('^part', k):
                parts.append(request.POST[k])
            if re.search('^note', k):
                part_notes.append(request.POST[k])
            if re.search('^quantity', k):
                part_quantities.append( request.POST[k])
        part_notes = part_notes[::-1]
        items = []
        k = 0
        for p in parts:
            if parts[k] is not None:
                    part = parts[k]
            else:
                    part = 0
            rma = 1
            data = {
                "rma": rma,
                'part': part,
                'quantity': part_quantities[k],
                'note': part_notes[k]
            }
            obj = {
                'form': ItemForm(data),
                'quantity': part_quantities[k]
            }
            items.append(obj)
            k += 1
        if rma_form.is_valid() is not True:
            error_count += 1
        for i in items:
            if  i['quantity']:
                if i['form'].is_valid() is not True:
                    error_count += 1

        new_items = []
        k = 0
        for i in items:
            if  i['quantity'] and i['quantity'] != '0':
                new_items.append(i['form'].as_table().replace('quantity"', 'quantity_'+str(k)+'"').replace('part"', 'part_'+str(k)+'"').replace('note"', 'note_'+str(k)+'"'))
            k += 1
        if len(new_items) == 0:
            item_mesg = 'YOU MUST SELECT SOME ITEMS'
            error_count += 1
            new_items = [ItemForm().as_table().replace('quantity"', 'quantity_'+str(0)+'"').replace('part"', 'part_'+str(0)+'"').replace('note"', 'note_'+str(0)+'"'),
                     ItemForm().as_table().replace('quantity"', 'quantity_'+str(1)+'"').replace('part"', 'part_'+str(1)+'"').replace('note"', 'note_'+str(1)+'"'),
                     ItemForm().as_table().replace('quantity"', 'quantity_'+str(2)+'"').replace('part"', 'part_'+str(2)+'"').replace('note"', 'note_'+str(2)+'"')]

        if error_count > 0:
            return render(request, 'return_merchandise_authorizations/create.html',
                {
                    'form': rma_form,
                    'customer_form': customer_form,
                    'items':new_items,
                    'msg': 'Please correct errors below<br>'+item_mesg,
                },
                context_instance=RequestContext(request))
        else:
            new_rma = rma_form.save()
            k = 0
            for p in parts:
                if parts[k]  and part_quantities[k]:
                    data = {
                        "rma": new_rma.id,
                        'part': parts[k],
                        'quantity': part_quantities[k],
                        'note': part_notes[k]
                    }
                    new_item = ItemFormWithRMA(data)
                    new_item.save()
                k += 1

            mail_new_rma_message(new_rma)
            return HttpResponseRedirect(reverse('view_rma', kwargs={'id': new_rma.id}))
class RmaUpdateView(UpdateView):
    template_name = 'return_merchandise_authorizations/edit.html'
    model = Rma
    fields = ['date']
    form_class = RmaForm

    @user_role_required_class_method
    def get(self, request, **kwargs):
        self.object = Rma.objects.get(id=self.kwargs['id'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        site_form = CustomerSiteNameEmptyDropdownForm()

        customer_form = CustomerNameDropdownForm()
        return render(request, self.template_name,
            {
                'rma': self.object,
                'form':form,
                'customer_form': customer_form,
                'site_form': site_form,
            },
            context_instance=RequestContext(request))


    @user_role_required_class_method
    def post(self, request, *args, **kwargs):
        data = {
            "id": request.POST['id'],
            "customer": request.POST['name'],
            'date': request.POST['date'],
            'case_number':  request.POST['case_number'],
            'reference_number':  request.POST['reference_number'],
            'contact':  request.POST['contact'],
            'contact_phone_number':  request.POST['contact_phone_number'],
            'address':  request.POST['address'],
            'issue':  request.POST['issue'],
            'shipping':  request.POST['shipping'],
            'outbound_tracking_number':  request.POST['outbound_tracking_number'],
            'return_tracking_number':  request.POST['return_tracking_number'],
            'root_cause_analysis':  request.POST['root_cause_analysis'],
            'phase':  request.POST['phase'],
            'repair_costs':  request.POST['repair_costs'],
            'last_modified_by':  request.user.id,
            'last_modified_on':  dt.now().strftime('%Y-%m-%d'),
        }
        self.object = Rma.objects.get(pk=data['id'])
        ref_checker = Rma.objects.filter(reference_number=data['reference_number'])
        self.form = RmaForm(data, instance=self.object)

        if self.form.is_valid():

            self.form.save()
            return redirect(self.get_success_url())
        else:
            site_form = CustomerSiteNameEmptyDropdownForm()
            customer_form = CustomerNameDropdownForm()
            return render(request, self.template_name,
                {
                    'rma': self.object,
                    'form': self.form,
                    'customer_form': customer_form,
                    'site_form': site_form,
                },
                context_instance=RequestContext(request))


    def get_object(self, queryset=None):
        obj = Rma.objects.get(id=self.kwargs['id'])
        obj.last_modified_by=self.request.user
        obj.last_modified_on=dt.now()
        return obj

    def get_success_url(self):
        return (reverse('view_rma', kwargs={'id': self.object.id}))


class RmaApproveView(UpdateView):
    template_name = 'return_merchandise_authorizations/approve.html'
    model = Rma
    fields = ['date']
    form_class = RmaApprovalForm
    def get(self, request, **kwargs):
        self.object = Rma.objects.get(id=self.kwargs['id'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        obj = Rma.objects.get(id=self.kwargs['id'])
        return obj

    def get_success_url(self):
        return (reverse('view_rma', kwargs={'id': self.object.id}))

    def get_initial(self):
        initial_vals = {
            'approved_on': dt.now().strftime('%Y-%m-%d'),
            'approved_by': self.request.user,
            'approved': 2,
            }
        return initial_vals

    def form_valid(self, form):
        form.save()
        mail_approved_rma_message(self.get_object())
        return HttpResponseRedirect(self.get_success_url())

class RmaDeleteView(DeleteView):
    model = Rma
    def get_object(self, queryset=None):
        obj = Rma.objects.get(id=self.kwargs['id'])
        return obj
    def get_success_url(self):
        return (reverse('home_page'))


    def get(self, request, **kwargs):
        user_group = Group.objects.get(name='user')
        if request.user.groups.filter(name='user').exists() is False:
            return render(request, 'errors/cannot_delete.html',
                  {},
        context_instance=RequestContext(request))
        else:

            return render(request, 'return_merchandise_authorizations/rma_confirm_delete.html',
                  {'object': self.get_object()},
        context_instance=RequestContext(request))
@login_required
def view(request, id):

    return render(request, 'return_merchandise_authorizations/view.html',
                  view_dict(id),
        context_instance=RequestContext(request))

@login_required
def download_rma_file(request, id):
    """
    Send a file through Django without loading the whole file into
    memory at once. The FileWrapper will turn the file object into an
    iterator for chunks of 8KB.
    """
    attach = RmaAttachment.objects.get(pk=id)

    filename = settings.RMA_ATTACHMENTS_DIR+attach.file.name.encode('ascii','ignore')[1:] # Select your file here.


    #wrapper = FileWrapper(file(filename))
    #response = HttpResponse(wrapper, content_type='text/plain')
    #response['Content-Length'] = os.path.getsize(filename)

    file = open(filename, 'rb')
    content = file.read()
    file.close
    response = HttpResponse(content, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=%s'%os.path.basename(filename)

    return response


@login_required
def manage_items(request, id):
    return render(request, 'return_merchandise_authorizations/manage_items.html',
                  view_dict(id),
        context_instance=RequestContext(request))

@login_required
def manage_attachments(request, id):
    return render(request, 'return_merchandise_authorizations/manage_attachments.html',
                  view_dict(id),
        context_instance=RequestContext(request))

@login_required
def manage_extra_fields(request, id):
    message = ''
    if request.method == 'GET':
        pass
    else:

        client = MongoClient()
        db = client[settings.MONGO_DB]
        extra_data = db.extra_data

        rma_extra_data = {}
        for d in request.POST:
            if d == '_id':
                continue
            elif d == 'rma_id':
                continue
            elif d == 'csrfmiddlewaretoken':
                continue
            else:
                rma_extra_data[d] = request.POST[d]
        extra_data.update({"_id":ObjectId(request.POST['_id'])},{"$set":rma_extra_data})
        message = 'Extra Data Saved'
    return render(request, 'return_merchandise_authorizations/manage_extra_fields.html',
        view_dict(id, message),
        context_instance=RequestContext(request))
def logout(request):
    """
    Removes the authenticated user's ID from the request and flushes their
    session data.
    """
    # Dispatch the signal before the user is logged out so the receivers have a
    # chance to find out *who* logged out.
    user = getattr(request, 'user', None)
    if hasattr(user, 'is_authenticated') and not user.is_authenticated():
        user = None
    user_logged_out.send(sender=user.__class__, request=request, user=user)

    # remember language choice saved to session
    # for backwards compatibility django_language is also checked (remove in 1.8)
    language = request.session.get(LANGUAGE_SESSION_KEY, request.session.get('django_language'))

    request.session.flush()

    if language is not None:
        request.session[LANGUAGE_SESSION_KEY] = language

    if hasattr(request, 'user'):
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()

    return render(request, 'return_merchandise_authorizations/index.html',
                  {'rmas': Rma.objects.all().order_by('-date')},
        context_instance=RequestContext(request))


def rma_login(request):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('home_page'))

    form = AuthenticationForm(data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect(reverse('home_page'))
            else:
                return HttpResponseRedirect(reverse('home_page'))
        else:
            return HttpResponseRedirect(reverse('home_page'))
    else:
        return HttpResponseRedirect(reverse('home_page'))