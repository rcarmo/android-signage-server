from django.contrib.admin import site, ModelAdmin

from django import forms, utils
from django.core import urlresolvers
from .models import Playlist, Asset, Device, Alert

from adminsortable.admin import NonSortableParentAdmin, SortableStackedInline, SortableTabularInline


class AssetInline(SortableTabularInline):
    model = Asset
    extra = 1

class DeviceAdmin(ModelAdmin):
    readonly_fields=('device_id','ip_address','mac_address','last_seen')
    list_display = ('name', 'active', 'related_playlist', 'device_id', 'mac_address', 'ip_address', 'last_seen')

    # These cannot be added, only modified or deleted
    def has_add_permission(self, request):
        return False

    def related_playlist(self, obj):
        if obj.playlist:
            link = urlresolvers.reverse("admin:signage_playlist_change", args=[obj.playlist.id])
            return u'<a href="%s">%s</a>' % (link, obj.playlist.name)
        return '(No playlist)'

    related_playlist.short_description = "Playlist"
    related_playlist.allow_tags = True # TODO: check this for injection exploits

class PlaylistAdmin(NonSortableParentAdmin):
    inlines = [AssetInline]
    list_display = ('name', 'asset_count')

    def asset_count(self, obj):
        return obj.asset_set.count()

    asset_count.short_description = "Assets"


class AlertAdmin(NonSortableParentAdmin):
    fields = ('name','active','when','devices')
    inlines = [AssetInline]
    list_display = ('name', 'active', 'asset_count', 'device_count', 'when')

    def asset_count(self, obj):
        return obj.asset_set.count()

    def device_count(self, obj):
        return map(lambda x: x.name, obj.devices.all())

    device_count.short_description = "Devices"
    asset_count.short_description = "Assets"

site.register(Alert, AlertAdmin)
site.register(Playlist, PlaylistAdmin)
site.register(Device, DeviceAdmin)