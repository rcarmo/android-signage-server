from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View
from .models import Playlist, Device

# Create your views here.

class PlaylistView(generic.TemplateView):
    template_name = 'playlist.json'
    try:
        default_playlist = Playlist.objects.get(name='Default')
    except:
        default_playlist = Playlist.objects.get(pk=1)

    def assets(self):
        return self.default_playlist.asset_set.all()

class DetailView(generic.DetailView):
    model = Playlist
    template_name = 'detail.json'