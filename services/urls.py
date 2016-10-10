from django.conf.urls import patterns, include, url
from services.views import numbered_returned_item_form
from services.views import returned_part_in_period_report
from services.views import returned_part_all_time_report
from services.views import customers_rmas_report
from services.views import customers_sites_dropdown
from services.views import returned_part_by_part_number_report
from services.views import returned_parts_by_quarter_by_site
from services.views import assign_role
urlpatterns = patterns('',
    url(r'numbered_return_item_form/(?P<number>[0-9]+)/$', numbered_returned_item_form, name='numbered_returned_item_form'),
    url(r'customers_rmas_report/(?P<number>[0-9]+)/$', customers_rmas_report, name='customers_rmas_report'),
    url(r'customers_sites_dropdown/(?P<number>[0-9]+)/$', customers_sites_dropdown, name='customers_sites_dropdown'),
    url(r'returned_part_in_period_report/(?P<part_number>[0-9]+)/(?P<start_year>\d{4})/(?P<start_month>\w{3})/(?P<start_day>\d{2})/(?P<end_year>\d{4})/(?P<end_month>\w{3})/(?P<end_day>\d{2})/$', returned_part_in_period_report, name='returned_part_in_period_report'),
    url(r'returned_part_all_time_report/(?P<part_number>[0-9]+)/$', returned_part_all_time_report, name='returned_part_all_time_report'),
    url(r'returned_part_by_part_number_report/(?P<part_number>[0-9]+)/$', returned_part_by_part_number_report, name='returned_part_by_part_number_report'),
    url(r'returned_parts_by_quarter_by_site/(?P<year>\d{4})/(?P<quarter>\w{1})/$', returned_parts_by_quarter_by_site, name='returned_parts_by_quarter_by_site'),
    url(r'assign_role/(?P<id>\d+)/(?P<role>[\w]+)/$', assign_role, name='assign_role'),


)
