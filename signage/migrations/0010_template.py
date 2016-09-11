# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-11 12:08
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signage', '0009_auto_20160911_1141'),
    ]

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Untitled Template', max_length=140)),
                ('url', models.CharField(max_length=512, validators=[django.core.validators.URLValidator()], verbose_name='URL')),
            ],
        ),
    ]
