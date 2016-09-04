from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Playlist(models.Model):
    name = models.CharField(max_length=128, default="Untitled")
    assets = models.TextField(default="{}")

class Alert(Playlist):
    pass

class Device(models.Model):
    identifier = models.CharField(max_length=128)
    name = models.CharField(max_length=128,default="Unnamed")
    alert = models.ForeignKey(Alert)