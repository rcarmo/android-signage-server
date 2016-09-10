from __future__ import unicode_literals

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from adminsortable.models import SortableMixin, SortableForeignKey

# Create your models here.

class Playlist(SortableMixin):
    name = models.CharField(max_length=140, default='Untitled Playlist', unique=True)
    # ordering field
    playlist_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        ordering = ['playlist_order']
        verbose_name_plural = 'Playlists'

    def __unicode__(self):
        return self.name

class Asset(SortableMixin):
    name = models.CharField(max_length=140, default='Untitled Asset')
    playlist = SortableForeignKey(Playlist)
    url = models.URLField(max_length=512, verbose_name="URL")
    duration = models.PositiveIntegerField(default=10, validators=[MaxValueValidator(1800),MinValueValidator(5),], verbose_name="Duration (s)")
    active = models.BooleanField(default=True)

    # ordering field
    asset_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        ordering = ['asset_order']

    def __unicode__(self):
        return self.name

class Device(models.Model):
    device_id = models.CharField(max_length=128, default='00deadbeef42', unique=True, editable=False)
    mac_address = models.CharField(max_length=17, default='00:de:ad:be:ef:42', unique=True,editable=False)
    ip_address = models.CharField(max_length=45, default='127.0.0.1', editable=False) # IPv6
    name = models.CharField(max_length=128,default='Unnamed Device')
    active = models.BooleanField(default=False)
    playlist = models.ForeignKey(Playlist, blank=True, null=True)

    def __unicode__(self):
        return self.name
