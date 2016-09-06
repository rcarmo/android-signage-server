from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View
from uuid import uuid5, NAMESPACE_URL
from .models import Playlist, Device

# Create your views here.

class PlaylistView(generic.TemplateView):
    template_name = 'playlist.json'

    def default_playlist(self):
        try:
            return Playlist.objects.get(name='Default')
        except:
            return Playlist.objects.get(pk=1)

    def uuid(self):
        acc = []
        for a in self.default_playlist().asset_set.order_by('asset_order'):
            acc.append((a.url, a.duration))
        return uuid5(NAMESPACE_URL, str(acc))

    def name(self):
        return self.default_playlist().name

    def assets(self):
        return self.default_playlist().asset_set.order_by('asset_order')

class DetailView(generic.DetailView):
    model = Playlist
    template_name = 'detail.json'