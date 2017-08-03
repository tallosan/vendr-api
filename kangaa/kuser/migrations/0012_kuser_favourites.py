# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-19 17:55
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kuser', '0011_dynamicclausenotification'),
    ]

    operations = [
        migrations.AddField(
            model_name='kuser',
            name='favourites',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.UUIDField(blank=True), default=[], size=None),
        ),
    ]
