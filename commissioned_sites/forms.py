__author__ = 'marc'
from django.forms import ModelForm
from django import forms
from django.forms import TextInput
from commissioned_sites.models import Network
from commissioned_sites.models import CommissionedSite
# Create the form class.
class SiteForm(ModelForm):
    class Meta:
        model = CommissionedSite
        fields = ['name', 'address', 'date', 'contact', 'contact_phone_number', 'cloud_ssh_tunnel_port', 'number_of_installed_energy_managers',\
    'number_of_installed_energy_managers_notes', 'number_of_installed_gateways', 'number_of_installed_sensor_units_and_control_units',\
    'number_of_installed_sensor_units_and_control_units_notes', 'number_of_installed_enlighted_room_controls',\
    'number_of_installed_enlighted_room_controls_notes',\
    'sensor_type', 'software_version_of_energy_manager', 'software_version_of_gateway', 'software_version_of_sensor_unit',\
    'profiles_file', 'software_upgraded', 'last_modified_by', 'last_modified_on']



class NetworkFormWithSite(ModelForm):
    class Meta:
        model = Network
        fields = [ 'site', 'wireless_network_name', 'ssid', 'password',
                   'energy_manager_ip_address', 'energy_manager_username', 'energy_manager_password']


        widgets = {
            'site': TextInput(attrs={'readonly':'readonly', 'type':'hidden'}),
        }

class NetworkForm(ModelForm):
    class Meta:
        model = Network
        fields = [ 'wireless_network_name', 'ssid', 'password',
                   'energy_manager_ip_address', 'energy_manager_username', 'energy_manager_password']

