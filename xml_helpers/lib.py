__author__ = 'marc'
# this breaks print
#from __future__ import print_function
import os
import re
from datetime import datetime as dt
import xml.etree.ElementTree as ET
from commissioned_sites.models import CommissionedSite
from customers.models import Customer
from parts.models import Part
from commissioned_sites.models import Network
from django.db import IntegrityError
from uuid import uuid4
from return_merchandise_authorizations.settings import *
import string
import redis
import json
import time
from customers.models import Customer
from django.conf import settings
from django.core.urlresolvers import reverse
import unicodedata
import urllib
from django.template import Context
from django.template import Template
from django.template import loader
from commissioned_sites.templatetags.clean_address import MLStripper
from bs4 import BeautifulSoup

from garage.logger import logger
p = re.compile(r'<.*?>')
"""
library for routines shared accross django command scripts
"""
def utc_mktime(utc_tuple):
    """Returns number of seconds elapsed since epoch

    Note that no timezone are taken into consideration.

    utc tuple must be: (year, month, day, hour, minute, second)

    """

    if len(utc_tuple) == 6:
        utc_tuple += (0, 0, 0)
    return time.mktime(utc_tuple) - time.mktime((1970, 1, 1, 0, 0, 0, 0, 0, 0))

def datetime_to_timestamp(dt):
    """Converts a datetime object to UTC timestamp"""

    return int(utc_mktime(dt.timetuple()))
def remove_sessions_from_redis():
    r = redis.StrictRedis(host='localhost', port=6379, db=settings.SESSION_REDIS_DB)
    keys = r.keys('session:*')

    for k in keys:
        r.delete(k)
def load_customer_to_redis(c, r):

    from return_merchandise_authorizations.models import Rma
    rmas = Rma.objects.filter(customer=c).order_by('-date')

    t = loader.get_template('xml_helpers/clean_issue.html')
    returns = []
    for rma in rmas:
        filename_cleaned = ''
        if rma.sharepoint_origin_url:
            filename_cleaned = unicodedata.normalize('NFKD', rma.sharepoint_origin_url).encode('ascii','ignore')

        ctx = {
            'rma': rma,
        }
        issue = t.render(Context(ctx))

        url = reverse('view_rma', args=(), kwargs={'id': rma.id})
        retobj = {
            'id': rma.id,
            'ts': datetime_to_timestamp(rma.date),
            'date': rma.date.strftime('%m/%d/%Y'),
            'url': url,
            'share_point_url': urllib.quote_plus(filename_cleaned),
            'issue': issue,
            'case_number': rma.case_number
        }
        returns.append(retobj)
    cval = {
        'id': c.customer.id,
        'customer_name': c.customer.company_name,
        'site_name': c.name,
        'returns': returns,
    }
    r.set(c.name, json.dumps(cval))
def load_customers_to_redis():

    r = redis.StrictRedis(host='localhost', port=6379, db=settings.REDIS_DB)
    r.flushdb()

    customers = Customer.objects.all()

    for c in customers:
        load_customer_to_redis(c, r)
    print 'loaded rmas and customers to %s'%settings.REDIS_DB
def save_item(rma, name, text):

    from return_merchandise_authorizations.models import Item
    if name == Energy_Manager:
        description = 'Energy Manager'
    elif name == Gateway:
        description = 'Gateway'
    elif name == Sensor_Units:
        description = 'Sensor Units'
    elif name == Control_Units:
        description = 'Control Units'
    elif name == Ballast:
        description = 'Ballast'
    elif name == Ballast_Type_Model_Number:
        description = 'Ballast Type/Model Number'
    elif name == LED_Driver:
        description = 'LED Driver'
    elif name == LED_Tube_Lights:
        description = 'LED Tube Lights'
    elif name == Florescent_Tube_Light:
        description = 'Florescent Tube Light'
    elif name == SU_Cable_7ft:
        description = 'SU Cable 7ft'
    elif name == Gateway_Ethernet_Cable_300_Ft:
        description = 'Gateway Ethernet Cable - 300 Ft'
    elif name == Energy_Manager_Ethernet_Cable_1_FT:
        description = 'Energy Manager Ethernet Cable - 1 FT'
    elif name == Netgear_PoE_Switch:
        description = 'Netgear PoE Switch'
    elif name == Other:
        description = 'Other (specify)'
    else:
        description = 'Netgear PoE Switch'
    model_number = ''
    quantity = '0'
    pattern = '^[0-9]*'
    if text:
        print 'text - %s'%text.encode('utf8')

        m = re.match(pattern, text)
        if m.group(0):
            print 'match - %s'%m.group(0)
            quantity = m.group(0)
            model_number = re.sub(pattern, '', text.encode('utf8'))
        else:
            model_number = text
    if quantity==None:
        quantity='0'
    print quantity

    part, created = Part.objects.get_or_create(description=description, model_number=model_number)
    if text is not None:
        item = Item()
        item.part = part

        item.quantity = int(quantity.strip())
        item.rma = rma
        item.save()

def read_in_site_from_share_point_commissioned_site(filename, user):


        with open(filename, 'r') as content_file:
            content = content_file.read()
        tree = ET.fromstring(content.replace('my:', ''))
        addressSplitArray =  content.replace('my:', '').split('Address')
        addressXmlStr = addressSplitArray[1][1:].replace('xml:','')[:-2]
        soup = BeautifulSoup(addressXmlStr)
        print addressXmlStr

        s = MLStripper()

        s.feed(addressXmlStr)

        address = s.get_data()
        """
        addr_lines = soup.find_all('tr')
        address = ''
        for l in addr_lines:
            print l.string
            address += str(l.string)
        quit()
        """
        print 'Address - %s'%address
        siteNotesSplitArray =  content.replace('my:', '').split('SiteNotes')
        siteNotesXmlStr = siteNotesSplitArray[1][1:].replace('xml:','')[:-2]

        root = tree

        site_name = root.findall('SiteName')[0].text
        print 'Site Name: %s'%site_name
        contact = root.findall('Contact')[0].text
        print 'Contact: %s'%contact
        print 'Address: %s'%p.sub('', address)

        phone = root.findall('Phone')[0].text
        print 'Phone: %s'%phone
        if len(root.findall('Tunnel-SSH-Port')) > 0:
            cloud_ssh_tunnel_port = root.findall('Tunnel-SSH-Port')[0].text
        else:
            cloud_ssh_tunnel_port = ''
        print 'Tunnel-SSH-Port %s'%cloud_ssh_tunnel_port
        number_of_installed_energy_managers = root.findall('NumberEM')[0].text
        print 'Number of Energy Manager: %s'%number_of_installed_energy_managers
        number_of_installed_gateways = root.findall('NumberGW')[0].text
        print 'Number of Gateway: %s'%number_of_installed_gateways
        number_of_installed_sensor_units_and_control_units = root.findall('NumberSU')[0].text
        print 'Number of Sensor Unit: %s'%number_of_installed_sensor_units_and_control_units

        number_of_installed_enlighted_room_controls = root.findall('NumberERC')[0].text
        print 'Number of Enlighted Room Controls: %s'%number_of_installed_enlighted_room_controls

        software_version_of_energy_manager = root.findall('SoftwareEM')[0].text
        print 'Software Version of Energy Manager: %s'%software_version_of_energy_manager
        software_version_of_gateway = root.findall('SoftwareGW')[0].text
        print 'Software Version of Gateway: %s'%software_version_of_gateway
        software_version_of_sensor_unit = root.findall('SoftwareSU')[0].text
        print 'Software Version of Sensor Unit: %s'%software_version_of_sensor_unit


        #profile_info = root.findall('ProfileInfo')[0].text
        #print 'ProfileInfo: %s'%profile_info

        #print 'Site Notes: %s'%siteNotesXmlStr

        sensor_type = root.findall('SensorType')[0].text
        print 'SensorType: %s'%sensor_type
        date = root.findall('Date')[0].text
        print 'Date: %s'%date


        wireless_network_name1 = root.findall('WAP1')[0].text
        ssid1 = root.findall('SSID')[0].text
        password1 = root.findall('PasswordWAP1')[0].text
        energy_manager_ip_address1 = root.findall('EMIP')[0].text
        energy_manager_username1 = root.findall('EM1User')[0].text
        energy_manager_password1 = root.findall('EM1Pass')[0].text

        print "First Network Name %s"%wireless_network_name1
        print "First SSID %s"%ssid1
        print "First Password %s"%password1
        print "First Energy Manager IP %s"%energy_manager_ip_address1
        print "First Energy Manager UserName %s"%energy_manager_username1
        print "First Energy Manager Password %s"%energy_manager_password1

        wireless_network_name2 = root.findall('WAP2')[0].text
        ssid2 = root.findall('SSID2')[0].text
        password2 = root.findall('PasswordWAP2')[0].text
        energy_manager_ip_address2 = root.findall('EM2IP')[0].text
        energy_manager_username2 = root.findall('EM2User')[0].text
        energy_manager_password2 = root.findall('EM2Pass')[0].text

        print "Second Network Name %s"%wireless_network_name2
        print "Second SSID %s"%ssid2
        print "Second Password %s"%password2
        print "Second Energy Manager IP %s"%energy_manager_ip_address2
        print "Second Energy Manager UserName %s"%energy_manager_username2
        print "Second Energy Manager Password %s"%energy_manager_password2

        wireless_network_name3 = root.findall('WAP3')[0].text
        ssid3 = root.findall('SSID3')[0].text
        password3 = root.findall('PasswordWAP3')[0].text
        energy_manager_ip_address3 = root.findall('EM3IP')[0].text
        energy_manager_username3 = root.findall('EM3User')[0].text
        energy_manager_password3 = root.findall('EM3Pass')[0].text
        site_notes = root.findall('SiteNotes')[0].text

        print "Third Network Name %s"%wireless_network_name3
        print "Third SSID %s"%ssid3
        print "Third Password %s"%password3
        print "Third Energy Manager IP %s"%energy_manager_ip_address3
        print "Third Energy Manager UserName %s"%energy_manager_username3
        print "Third Energy Manager Password %s"%energy_manager_password3
        print "first network %s %s"%(wireless_network_name1, ssid1)
        print "first network %s"%(energy_manager_ip_address1)
        site = CommissionedSite()
        site.name = site_name
        site.address = address
        site.date = date
        site.contact = contact
        site.contact_phone_number = phone
        site.cloud_ssh_tunnel_port = cloud_ssh_tunnel_port
        site.number_of_installed_gateways = number_of_installed_gateways
        #
        if number_of_installed_energy_managers.strip().isdigit():
            site.number_of_installed_energy_managers = number_of_installed_energy_managers.strip()
        else:

            site.number_of_installed_energy_managers = 0
            site.number_of_installed_energy_managers_notes = number_of_installed_energy_managers
        #
        if number_of_installed_sensor_units_and_control_units.strip().isdigit():
            site.number_of_installed_sensor_units_and_control_units = number_of_installed_sensor_units_and_control_units.strip()
        else:

            site.number_of_installed_sensor_units_and_control_units = 0
            site.number_of_installed_sensor_units_and_control_units_notes = number_of_installed_sensor_units_and_control_units
        #
        if number_of_installed_enlighted_room_controls and number_of_installed_enlighted_room_controls.strip().isdigit():
            site.number_of_installed_enlighted_room_controls = number_of_installed_enlighted_room_controls.strip()
        else:

            site.number_of_installed_enlighted_room_controls = 0
            site.number_of_installed_enlighted_room_controls_notes = number_of_installed_enlighted_room_controls


        site.software_version_of_energy_manager = software_version_of_energy_manager
        site.software_version_of_gateway = software_version_of_gateway
        site.software_version_of_sensor_unit = software_version_of_sensor_unit
        #site.profile_info = profile_info
        site.sensor_type = sensor_type
        site.sharepoint_origin = 2
        site.sharepoint_origin_url = os.path.basename(filename)

        site.last_modified_by = user
        site.notes = site_notes
        print site
        site.save()
        if energy_manager_ip_address1 is not None:
            network = Network()
            network.wireless_network_name = wireless_network_name1
            network.password = password1
            network.ssid = ssid1
            network.energy_manager_ip_address = energy_manager_ip_address1
            network.energy_manager_username = energy_manager_username1
            network.energy_manager_password = energy_manager_password1
            network.site = site
            network.save()

        if energy_manager_ip_address2 is not None:
            network = Network()
            network.wireless_network_name = wireless_network_name2
            network.password = password2
            network.ssid = ssid2
            network.energy_manager_ip_address = energy_manager_ip_address2
            network.energy_manager_username = energy_manager_username2
            network.energy_manager_password = energy_manager_password2
            network.site = site
            network.save()

        if energy_manager_ip_address3 is not None:
            network = Network()
            network.wireless_network_name = wireless_network_name3
            network.password = password3
            network.ssid = ssid3
            network.energy_manager_ip_address = energy_manager_ip_address3
            network.energy_manager_username = energy_manager_username3
            network.energy_manager_password = energy_manager_password3
            network.site = site
            network.save()

