# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-05 20:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0008_transaction_contracts_equal'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='_dampen',
            field=models.BooleanField(default=False),
        ),
    ]
