# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-11 08:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signage', '0007_auto_20160910_2031'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='parameters',
            field=models.CharField(default='', max_length=512),
            preserve_default=False,
        ),
    ]
