# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-02 23:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kuser', '0008_auto_20170702_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='prof_pic',
            field=models.ImageField(blank=True, default='profiles/default.svg', upload_to='profiles/'),
        ),
    ]