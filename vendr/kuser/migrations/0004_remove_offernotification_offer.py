# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-02 22:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kuser', '0003_remove_kuser_uuid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offernotification',
            name='offer',
        ),
    ]