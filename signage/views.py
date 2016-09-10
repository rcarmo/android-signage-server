from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View
from uuid import uuid5, NAMESPACE_URL
from .models import Playlist, Device

# Create your views here.

# TODO: handle alerts

class PlaylistView(generic.TemplateView):
    template_name = 'playlist.json'
    default_playlist = None

    def get_or_update_device(self):
        try:
            device = Device.objects.get(device_id=self.kwargs['device_id'])
            dirty = False
            if device.ip_address != self.kwargs['ip_address']:
                device.ip_address = self.kwargs['ip_address']
                dirty = True
            if device.mac_address != self.kwargs['mac_address']:
                device.mac_address = self.kwargs['mac_address']
                dirty = True
            if dirty:
                device.save()
        except:
            device = Device(device_id = self.kwargs['device_id'],
                     mac_address = self.kwargs['mac_address'],
                     ip_address = self.kwargs['ip_address'])
            device.save()
            
        return device


    def get_playlist(self):
        device = self.get_or_update_device()
        if device.active:
            if device.playlist:
                return device.playlist
            try:
                return Playlist.objects.get(name='Default')
            except:
                return Playlist.objects.get(pk=1)
        return Playlist()


    def uuid(self):
        acc = []
        for a in self.get_playlist().asset_set.order_by('asset_order'):
            acc.append((a.url, a.duration))
        return uuid5(NAMESPACE_URL, str(acc))


    def name(self):
        return self.get_playlist().name


    def assets(self):
        return self.get_playlist().asset_set.order_by('asset_order')


class DetailView(generic.DetailView):
    model = Playlist
    template_name = 'detail.json'