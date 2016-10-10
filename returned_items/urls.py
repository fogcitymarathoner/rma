from django.conf.urls import patterns, include, url
from returned_items.views import index
from returned_items.views import move_items
from returned_items.views import ReturnedItemCreateView
from returned_items.views import ReturnedItemUpdateView
from returned_items.views import ReturnedItemDeleteView
from returned_items.views import move_items_confirm
from django.contrib.auth.decorators import login_required
urlpatterns = patterns('',
    url(r'^$', index, name='list_returned_items'),
    url(r'move_items$', move_items, name='move_returned_items'),
    url(r'move_items_confirm$', move_items_confirm, name='confirm_move_items'),
    url(r'create/(?P<id>\d+)$', login_required(ReturnedItemCreateView.as_view()), name='create_returned_item'),
    url(r'edit/(?P<id>\d+)$', login_required(ReturnedItemUpdateView.as_view()), name='edit_returned_item'),
    url(r'delete/(?P<id>\d+)$', login_required(ReturnedItemDeleteView.as_view()), name='delete_returned_item'),
)
