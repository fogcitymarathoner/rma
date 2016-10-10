from django.contrib import admin
from commissioned_sites.models import CommissionedSite
from commissioned_sites.models import Network
from commissioned_sites.models import SiteAttachment
class NetworkInline(admin.TabularInline):
    model = Network


class AttachInline(admin.TabularInline):
    model = SiteAttachment

class CommissionedSiteAdmin(admin.ModelAdmin):
    inlines = [
        NetworkInline,
        AttachInline,
    ]


admin.site.register(CommissionedSite, CommissionedSiteAdmin)
