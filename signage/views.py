from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, DetailView
from django.utils import timezone
from uuid import uuid5, NAMESPACE_URL
from .models import Playlist, Device, Alert
from datetime import datetime

# Create your views here.

# TODO: handle alerts

class PlaylistView(TemplateView):
    template_name = 'playlist.json'
    playlist = None

    def update_device(self, kwargs):
        try:
            device = Device.objects.get(device_id=kwargs['device_id'])
            dirty = False
            if device.ip_address != kwargs['ip_address']:
                device.ip_address = kwargs['ip_address']
                dirty = True
            if device.mac_address != kwargs['mac_address']:
                device.mac_address = kwargs['mac_address']
        except:
            device = Device(device_id = kwargs['device_id'],
                     mac_address = kwargs['mac_address'],
                     ip_address = kwargs['ip_address'])
        device.save()
        return device


    def get_context_data(self, **kwargs):
        context = super(PlaylistView, self).get_context_data(**kwargs)
        device = self.update_device(kwargs)
        alert = False
        print device
        if device.active:
            # do we have pending alerts for this device?
            print "active"
            alerts = list(Alert.objects.filter(
                active=True,
                when__lte=timezone.now(),
                devices__pk__exact=device.pk
            ).exclude(
                shown_on__pk__exact=device.pk
            ).order_by('when').distinct()[:1])
            print alerts
            if alerts:
                alert = alerts[0]
                self.alert = True
                alert.shown_on.add(device)
                if set(list(alert.shown_on.all())) == set(list(alert.devices.all())):
                    alert.active = False 
                alert.save()
                playlist = alert
                context['alert'] = True
            elif device.playlist:
                playlist = device.playlist
            else:
                try:
                    playlist = Playlist.objects.get(name='Default')
                except:
                    playlist = Playlist.objects.get(pk=1)
        else:
            playlist = Playlist()
        context['playlist'] = playlist
        context['uuid'] = self.uuid(playlist)
        context['assets'] = playlist.asset_set.order_by('asset_order')

        return context

    def uuid(self, playlist):
        acc = []
        for a in playlist.asset_set.order_by('asset_order'):
            acc.append((a.url, a.duration, a.active, a.kind))
        return uuid5(NAMESPACE_URL, str(acc))

class DetailView(DetailView):
    model = Playlist
    template_name = 'detail.json'