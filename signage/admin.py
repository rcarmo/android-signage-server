from django.contrib.admin import site, ModelAdmin, SimpleListFilter
from django.utils import timezone
from datetime import datetime, timedelta
from django import forms, utils
from django.core import urlresolvers
from .models import Playlist, Asset, Device, Alert

from adminsortable.admin import NonSortableParentAdmin, SortableStackedInline, SortableTabularInline


class AssetInline(SortableTabularInline):
    model = Asset
    extra = 1


class ActiveFilter(SimpleListFilter):
    title = 'State'
    parameter_name = 'active'

    def lookups(self, request, obj):
        return [(True,"Active"),(False,"Inactive")]

    def queryset(self, request, qs):
        if not self.value():
            return qs
        return qs.filter(active=self.value())


class PlaylistFilter(SimpleListFilter):
    title = 'Playlist'
    parameter_name = 'playlist'

    def lookups(self, request, obj):
        playlists = set(list(Device.objects.values_list("playlist", flat=True)))
        return sorted(map(lambda x: (0 if x == None else x, Playlist.objects.get(pk=x) if x else '(No playlist)'), playlists))

    def queryset(self, request, qs):
        print self.value()
        if self.value() == None:
            return qs
        elif int(self.value()) == 0:
            return qs.filter(playlist__isnull=True)
        return qs.filter(playlist__pk=self.value())


class SeenFilter(SimpleListFilter):
    title = 'Last Seen'
    parameter_name = 'last_seen'

    def lookups(self, request, obj):
        return [
            (60, 'Last Minute'),
            (3600, 'Last Hour'),
            (86400, 'Last 24h'),
            (-86400, 'Yesterday'),
            (-86400*7, 'Last Week')
        ]

    def queryset(self, request, qs):
        if not self.value():
            return qs
        limit = int(self.value())
        if limit < 0:
            return qs.filter(last_seen__lte=(timezone.now() + timedelta(seconds=limit)))
        else:
            return qs.filter(last_seen__gte=(timezone.now() - timedelta(seconds=limit)))


class DeviceAdmin(ModelAdmin):
    readonly_fields=('device_id','ip_address','mac_address','last_seen')
    list_display = ('name', 'active', 'related_playlist', 'device_id', 'mac_address', 'ip_address', 'last_seen')
    list_filter = (ActiveFilter,PlaylistFilter,SeenFilter)

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


class DeviceFilter(SimpleListFilter):
    title = 'Device'
    parameter_name = 'device'

    def lookups(self, request, obj):
        devices = set(list(Alert.objects.values_list("devices", flat=True)))
        return sorted(map(lambda x: (x, Device.objects.get(pk=x)), devices))

    def queryset(self, request, qs):
        if not self.value():
            return qs
        return qs.filter(devices__pk__exact=self.value())


class DeliveryFilter(SimpleListFilter):
    title = 'Delivered To'
    parameter_name = 'shown'

    def lookups(self, request, obj):
        devices = set(list(Alert.objects.values_list("shown_on", flat=True)))
        return sorted(map(lambda x: (x, Device.objects.get(pk=x)), devices))

    def queryset(self, request, qs):
        if not self.value():
            return qs
        return qs.filter(devices__pk__exact=self.value())



class AlertAdmin(NonSortableParentAdmin):
    fields = ('name','active','when','devices')
    inlines = [AssetInline]
    list_display = ('name', 'active', 'asset_count', 'total_duration', 'device_names', 'delivered_to', 'when')
    list_filter = (ActiveFilter,DeviceFilter,DeliveryFilter)

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