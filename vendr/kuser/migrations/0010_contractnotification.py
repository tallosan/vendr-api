# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-05 19:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kuser', '0009_auto_20170702_2351'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractNotification',
            fields=[
                ('transactionnotification_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='kuser.TransactionNotification')),
                ('contract', models.UUIDField()),
            ],
            options={
                'abstract': False,
            },
            bases=('kuser.transactionnotification',),
        ),
    ]
