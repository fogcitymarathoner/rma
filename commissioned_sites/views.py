import json
import redis
import os
import re
from bson.objectid import ObjectId
from datetime import datetime as dt
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.http import HttpResponse
from django.views.generic.edit import UpdateView
from django.views.generic.edit import CreateView
from django.views.generic import DeleteView
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.conf import settings
from pymongo import MongoClient
from commissioned_sites.models import CommissionedSite
from commissioned_sites.models import Network
from commissioned_sites.models import SiteAttachment
from commissioned_sites.forms import SiteForm
from commissioned_sites.forms import NetworkForm
from commissioned_sites.forms import NetworkFormWithSite

from return_merchandise_authorizations.lib import mail_new_site_message
@login_required
def index(request):
    """
    the commissioned sites list page
    :param request:
    :return:
    """
    return render(request, 'commissioned_sites/index.html',
                  {'sites': CommissionedSite.objects.all().order_by('-date')},
        context_instance=RequestContext(request))

@login_required
def view(request, id):
    site = CommissionedSite.objects.get(id=id)
    networks = Network.objects.filter(site=site)
    readable_networks = []
    for i in networks:
        new_i = {
            'wireless_network_name': i.wireless_network_name,
            'ssid': i.ssid,
            'energy_manager_ip_address': i.energy_manager_ip_address
        }
        readable_networks.append(new_i)

    attachs = SiteAttachment.objects.filter(site=site)
    attachments = []
    for i in attachs:
        new_i = {
            'file': i.file,
            'id': i.id,
        }
        attachments.append(new_i)
    return render(request, 'commissioned_sites/view.html',
                  {'site': site,
                   'networks': readable_networks,
                   'attachments': attachments,
                  },
        context_instance=RequestContext(request))



@login_required
def download_site_file(request, id):
    """
    Send a file through Django without loading the whole file into
    memory at once. The FileWrapper will turn the file object into an
    iterator for chunks of 8KB.
    """
    attach = SiteAttachment.objects.get(pk=id)

    filename = settings.COMMISSIONED_SITES_ATTACHMENTS_DIR+attach.file.name.encode('ascii','ignore')[1:] # Select your file here.

    file = open(filename, 'rb')
    content = file.read()
    file.close
    response = HttpResponse(content, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=%s'%os.path.basename(filename)

    return response

@login_required
def download_site_profile_file(request, id):
    """
    Send a file through Django without loading the whole file into
    memory at once. The FileWrapper will turn the file object into an
    iterator for chunks of 8KB.
    """
    site = CommissionedSite.objects.get(pk=id)

    filename = settings.COMMISSIONED_SITES_PROFILES_DIR+site.profiles_file.name.encode('ascii','ignore')[1:] # Select your file here.

    file = open(filename, 'rb')
    content = file.read()
    file.close
    response = HttpResponse(content, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=%s'%os.path.basename(filename)

    return response



class SiteUpdateView(UpdateView):
    template_name = 'commissioned_sites/edit.html'
    model = CommissionedSite
    fields = ['date']
    form_class = SiteForm
    def get(self, request, **kwargs):
        self.object = CommissionedSite.objects.get(id=self.kwargs['id'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        obj = CommissionedSite.objects.get(id=self.kwargs['id'])
        obj.last_modified_by=self.request.user
        obj.last_modified_on=dt.now()
        return obj

    def get_success_url(self):
        return (reverse('view_site', kwargs={'id': self.object.id}))


class SiteDeleteView(DeleteView):
    model = CommissionedSite
    def get_object(self, queryset=None):
        obj = CommissionedSite.objects.get(id=self.kwargs['id'])
        return obj
    def get_success_url(self):
        return (reverse('commissioned_sites'))

# not an action
def view_dict(id, message=None):

    r = redis.StrictRedis(host='localhost', port=6379, db=settings.SESSION_REDIS_DB)
    rfields = json.loads(r.get(settings.SUB_URL.replace('/','')+':commissioned_site_extra_data'))

    client = MongoClient()
    db = client[settings.MONGO_DB]
    extra_data = db.extra_data

    site_extra_data = extra_data.find_one({"site_id": id})

    # initialize mongo data if None
    if site_extra_data == None:
        site_extra_data = {
            'site_id': id,
        }
        for f in rfields:
            site_extra_data[f] = ''

        extra_data.insert(site_extra_data)
    # add new fields that have been added since last save
    for f in rfields:
        if f not in site_extra_data.keys():
            site_extra_data[f] = ''
    print site_extra_data
    site = CommissionedSite.objects.get(id=id)

    networks = Network.objects.filter(site=site)
    readable_networks = []
    for i in networks:
        new_n = {
            'id': i.id,
            'wireless_network_name': i.wireless_network_name,
            'ssid': i.ssid,
            'password': i.password,
            'energy_manager_ip_address': i.energy_manager_ip_address,
            'energy_manager_username': i.energy_manager_username,
            'energy_manager_password': i.energy_manager_password,
        }
        readable_networks.append(new_n)


    attachs = SiteAttachment.objects.filter(site=site)
    attachments = []
    for i in attachs:
        new_i = {
            'file': i.file,
            'id': i.id,
        }
        attachments.append(new_i)
    return {'site': site,
           'networks': readable_networks,
           'attachments': attachments,
           'site_extra_data': site_extra_data,
           'message': message
          }

@login_required
def manage_networks(request, id):
    return render(request, 'commissioned_sites/manage_networks.html',
                  view_dict(id),
        context_instance=RequestContext(request))

@login_required
def manage_attachments(request, id):
    return render(request, 'commissioned_sites/manage_attachments.html',
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

        site_extra_data = {}
        for d in request.POST:
            if d == '_id':
                continue
            elif d == 'site_id':
                continue
            elif d == 'csrfmiddlewaretoken':
                continue
            else:
                site_extra_data[d] = request.POST[d]
        extra_data.update({"_id": ObjectId(request.POST['_id'])},{"$set":site_extra_data})
        message = 'Extra Data Saved'
    return render(request, 'commissioned_sites/manage_extra_fields.html',
        view_dict(id, message),
        context_instance=RequestContext(request))


class NetworkCreateView(CreateView):
    template_name = 'returned_items/create.html'
    model = Network
    fields = ['date']
    form_class = NetworkForm

    def get_success_url(self):
        return (reverse('manage_networks', kwargs={'id': self.object.site.id}))
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

    #override form_valid method
    def form_valid(self, form):
        #save cleaned post data
        clean = form.cleaned_data
        context = {}
        self.object = context.save(clean)
        return super(NetworkUpdateView, self).form_valid(form)

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
        return (reverse('manage_networks', kwargs={'id': self.object.site.id}))

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
        return (reverse('manage_networks', kwargs={'id': self.object.site.id}))


@login_required
def create(request):

    if request.method == 'GET':
        data = {
            'last_modified_by': request.user,
            'last_modified_on': dt.now(),
        }
        form = SiteForm(initial=data)

        networks = [NetworkForm().as_table().replace('wireless_network_name"', 'wireless_network_name_'+str(0)+'"').replace('ssid"', 'ssid_'+str(0)+'"').replace('password"', 'password_'+str(0)+'"').replace('energy_manager_ip_address"', 'energy_manager_ip_address_'+str(0)+'"').replace('energy_manager_username"', 'energy_manager_username_'+str(0)+'"').replace('energy_manager_password"', 'energy_manager_password_'+str(0)+'"'),
                 NetworkForm().as_table().replace('wireless_network_name"', 'wireless_network_name_'+str(1)+'"').replace('ssid"', 'ssid_'+str(1)+'"').replace('password"', 'password_'+str(1)+'"').replace('energy_manager_ip_address"', 'energy_manager_ip_address_'+str(1)+'"').replace('energy_manager_username"', 'energy_manager_username_'+str(1)+'"').replace('energy_manager_password"', 'energy_manager_password_'+str(1)+'"'),
                 NetworkForm().as_table().replace('wireless_network_name"', 'wireless_network_name_'+str(2)+'"').replace('ssid"', 'ssid_'+str(2)+'"').replace('password"', 'password_'+str(2)+'"').replace('energy_manager_ip_address"', 'energy_manager_ip_address_'+str(2)+'"').replace('energy_manager_username"', 'energy_manager_username_'+str(2)+'"').replace('energy_manager_password"', 'energy_manager_password_'+str(2)+'"')]
        return render(request, 'commissioned_sites/create.html',
            {
                'form':form,
                'networks':networks,
            },
            context_instance=RequestContext(request))


    if request.method == 'POST':
        error_count = 0
        network_mesg = ''
        site_form = SiteForm(request.POST, request.FILES)
        """
        gather networks into 6 arrays
            wireless_network_name
            ssid
            password
            energy_manager_ip_address
            energy_manager_username
            energy_manager_password

        """
        wireless_network_names = []
        ssids = []
        passwords = []
        energy_manager_ip_addresses = []
        energy_manager_usernames = []
        energy_manager_passwords = []
        for k in sorted(request.POST.keys()):
            if re.search('^wireless_network_name', k):
                wireless_network_names.append(request.POST[k])
            if re.search('^ssid', k):
                ssids.append(request.POST[k])
            if re.search('^password', k):
                passwords.append( request.POST[k])
            if re.search('^energy_manager_ip_address', k):
                energy_manager_ip_addresses.append(request.POST[k])
            if re.search('^energy_manager_username', k):
                energy_manager_usernames.append(request.POST[k])
            if re.search('^energy_manager_password', k):
                energy_manager_passwords.append( request.POST[k])

        print wireless_network_names
        print ssids
        print passwords
        print energy_manager_ip_addresses
        print energy_manager_usernames
        print energy_manager_passwords
        k = 0
        networks = []
        for p in wireless_network_names:
            print p
            print k
            if wireless_network_names[k] is not None:
                    wireless_network_name = wireless_network_names[k]
            else:
                    wireless_network_name = 0
            site = 1
            data = {
                "site": site,
                'wireless_network_name': wireless_network_name,
                'ssid': ssids[k],
                'password': passwords[k],
                'energy_manager_ip_address': energy_manager_ip_addresses[k],
                'energy_manager_username': energy_manager_usernames[k],
                'energy_manager_password': energy_manager_passwords[k]
            }
            obj = {
                'form': NetworkForm(data),
            }
            networks.append(obj)
            k += 1
        if site_form.is_valid() is not True:
            error_count += 1
        for i in networks:
            if i['form'].is_valid() is not True:
                error_count += 1

        new_networks = []
        k = 0
        for i in networks:
            new_networks.append(i['form'].as_table().replace('wireless_network_name"', 'wireless_network_name_'+str(2)+'"').replace('ssid"', 'ssid_'+str(2)+'"').replace('password"', 'password_'+str(2)+'"').replace('energy_manager_ip_address"', 'energy_manager_ip_address_'+str(2)+'"').replace('energy_manager_username"', 'energy_manager_username_'+str(2)+'"').replace('energy_manager_password"', 'energy_manager_password_'+str(2)+'"'))
            k += 1
        if len(new_networks) == 0:
            network_mesg = 'YOU MUST SET A NETWORK'
            error_count += 1

            new_networks = [NetworkForm().as_table().replace('wireless_network_name"', 'wireless_network_name_'+str(0)+'"').replace('ssid"', 'ssid_'+str(0)+'"').replace('password"', 'password_'+str(0)+'"').replace('energy_manager_ip_address"', 'energy_manager_ip_address_'+str(0)+'"').replace('energy_manager_username"', 'energy_manager_username_'+str(0)+'"').replace('energy_manager_password"', 'energy_manager_password_'+str(0)+'"'),
                     NetworkForm().as_table().replace('wireless_network_name"', 'wireless_network_name_'+str(1)+'"').replace('ssid"', 'ssid_'+str(1)+'"').replace('password"', 'password_'+str(1)+'"').replace('energy_manager_ip_address"', 'energy_manager_ip_address_'+str(1)+'"').replace('energy_manager_username"', 'energy_manager_username_'+str(1)+'"').replace('energy_manager_password"', 'energy_manager_password_'+str(1)+'"'),
                     NetworkForm().as_table().replace('wireless_network_name"', 'wireless_network_name_'+str(2)+'"').replace('ssid"', 'ssid_'+str(2)+'"').replace('password"', 'password_'+str(2)+'"').replace('energy_manager_ip_address"', 'energy_manager_ip_address_'+str(2)+'"').replace('energy_manager_username"', 'energy_manager_username_'+str(2)+'"').replace('energy_manager_password"', 'energy_manager_password_'+str(2)+'"')]

        if error_count > 0:
            return render(request, 'commissioned_sites/create.html',
                {
                    'form': site_form,
                    'networks': new_networks,
                    'msg': 'Please correct errors below<br>'+network_mesg
                },
                context_instance=RequestContext(request))
        else:
            new_site = site_form.save()
            k = 0
            for p in wireless_network_names:
                if wireless_network_names[k]:
                    data = {
                        "site": new_site.id,

                        'wireless_network_name': wireless_network_names[k],
                        'ssid': ssids[k],
                        'password': passwords[k],
                        'energy_manager_ip_address': energy_manager_ip_addresses[k],
                        'energy_manager_username': energy_manager_usernames[k],
                        'energy_manager_password': energy_manager_passwords[k],
                    }
                    new_network= NetworkFormWithSite(data)
                    new_network.save()
                k += 1

            mail_new_site_message(new_site)
            return HttpResponseRedirect(reverse('view_site', kwargs={'id': new_site.id}))