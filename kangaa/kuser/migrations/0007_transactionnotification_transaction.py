# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-02 22:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kuser', '0006_offernotification_offer'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionnotification',
            name='transaction',
            field=models.UUIDField(default='41fb527a-d4bb-452b-83a6-fb8bece1b533'),
            preserve_default=False,
        ),
    ]
