# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-11 20:23
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kproperty', '0005_auto_20170710_2014'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='geo_point',
            field=django.contrib.gis.db.models.fields.PointField(null=True, srid=4326),
        ),
    ]