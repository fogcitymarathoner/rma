from django.contrib import admin
from return_merchandise_authorizations.models import Rma
from return_merchandise_authorizations.models import Item
from return_merchandise_authorizations.models import RmaAttachment

class ItemInline(admin.TabularInline):
    model = Item


class AttachInline(admin.TabularInline):
    model = RmaAttachment

class RmaAdmin(admin.ModelAdmin):
    list_display = ('date', 'customer', 'case_number', 'reference_number', 'address')
    search_fields = ('case_number', 'reference_number', 'address', 'issue')

    inlines = [
        ItemInline,
        AttachInline
    ]

#
admin.site.register(Rma, RmaAdmin)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('note', 'quantity')

#
admin.site.register(Item, ItemAdmin)