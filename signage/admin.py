from django.contrib import admin

from django import forms, utils
from .models import Playlist, Asset, Device
from adminsortable.admin import NonSortableParentAdmin, SortableStackedInline, SortableTabularInline


class AssetInline(SortableTabularInline):
    model = Asset
    extra = 1

class DeviceAdmin(admin.ModelAdmin):
    readonly_fields=('device_id','ip_address','mac_address')

    # These cannot be added, only modified or deleted
    def has_add_permission(self, request):
        return False

class PlaylistAdmin(NonSortableParentAdmin):
    inlines = [AssetInline]

admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(Device, DeviceAdmin)