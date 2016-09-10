from django.contrib import admin

from django import forms, utils
from django.core import urlresolvers
from .models import Playlist, Asset, Device

from adminsortable.admin import NonSortableParentAdmin, SortableStackedInline, SortableTabularInline


class AssetInline(SortableTabularInline):
    model = Asset
    extra = 1

class DeviceAdmin(admin.ModelAdmin):
    readonly_fields=('device_id','ip_address','mac_address')
    list_display = ('name', 'active', 'related_playlist', 'device_id', 'mac_address', 'ip_address')

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

admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(Device, DeviceAdmin)