# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-04 21:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=128)),
                ('name', models.CharField(default='Unnamed', max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Untitled', max_length=128)),
                ('assets', models.TextField(default='{}')),
            ],
        ),
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('playlist_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='signage.Playlist')),
            ],
            bases=('signage.playlist',),
        ),
        migrations.AddField(
            model_name='device',
            name='alert',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signage.Alert'),
        ),
    ]
