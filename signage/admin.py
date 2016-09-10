from django.contrib.admin import site, ModelAdmin, SimpleListFilter

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
    list_display = ('name', 'asset_count', 'total_duration')

    def get_queryset(self, request):    
        qs = super(PlaylistAdmin, self).get_queryset(request)
        return qs.filter(alert__isnull=True)

    def asset_count(self, obj):
        return obj.asset_set.count()

    def total_duration(self, obj):
        return reduce(lambda x, y: x + y.duration, obj.asset_set.all(), 0)

    asset_count.short_description = "Assets"


class AlertAdmin(NonSortableParentAdmin):
    fields = ('name','active','when','devices')
    inlines = [AssetInline]
    list_display = ('name', 'active', 'asset_count', 'total_duration', 'device_names', 'delivered_to', 'when')

    def save_model(self, request, obj, form, change):
        obj.shown_on.clear()
        obj.save()

    def asset_count(self, obj):
        return obj.asset_set.count()

    def total_duration(self, obj):
        return reduce(lambda x, y: x + y.duration, obj.asset_set.all(), 0)

    def device_names(self, obj):
        return map(lambda x: x.name, obj.devices.all())

    def delivered_to(self, obj):
        return map(lambda x: x.name, obj.shown_on.all())


    device_names.short_description = "Devices"
    asset_count.short_description = "Assets"

site.register(Alert, AlertAdmin)
site.register(Playlist, PlaylistAdmin)
site.register(Device, DeviceAdmin)