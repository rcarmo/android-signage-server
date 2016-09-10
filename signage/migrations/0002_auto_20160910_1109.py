# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-10 11:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signage', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='identifier',
        ),
        migrations.AddField(
            model_name='device',
            name='device_id',
            field=models.CharField(default='00deadbeef42', editable=False, max_length=128, unique=True),
        ),
        migrations.AddField(
            model_name='device',
            name='ip_address',
            field=models.CharField(default='127.0.0.1', editable=False, max_length=45),
        ),
        migrations.AddField(
            model_name='device',
            name='mac_address',
            field=models.CharField(default='00:de:ad:be:ef:42', editable=False, max_length=17, unique=True),
        ),
    ]
