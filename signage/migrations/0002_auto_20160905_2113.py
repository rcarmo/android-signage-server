# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-05 21:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signage', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='asset',
            old_name='category',
            new_name='playlist',
        ),
    ]