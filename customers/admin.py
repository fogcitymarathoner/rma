from django.contrib import admin
from customers.models import Customer
from return_merchandise_authorizations.models import Rma

class RmaInline(admin.TabularInline):
    model = Rma


class CustomerAdmin(admin.ModelAdmin):
    inlines = [
        RmaInline,
    ]


admin.site.register(Customer, CustomerAdmin)
