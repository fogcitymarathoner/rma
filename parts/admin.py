from django.contrib import admin
from parts.models import Part


class PartAdmin(admin.ModelAdmin):
    list_display = ('description', 'model_number')
    search_fields = ('description', 'model_number')

#
admin.site.register(Part, PartAdmin)

