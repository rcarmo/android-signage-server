# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-05 21:38
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('signage', '0003_auto_20160905_2125'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='title',
            field=models.CharField(default='Untitled Asset', max_length=140),
        ),
        migrations.AddField(
            model_name='device',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='device',
            name='playlist',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='signage.Playlist'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='duration',
            field=models.PositiveIntegerField(default=10, validators=[django.core.validators.MaxValueValidator(1800), django.core.validators.MinValueValidator(5)], verbose_name='Duration (s)'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='url',
            field=models.URLField(max_length=512, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='device',
            name='name',
            field=models.CharField(default='Unnamed Device', max_length=128),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='title',
            field=models.CharField(default='Untitled Playlist', max_length=140),
        ),
    ]
