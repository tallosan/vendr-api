# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-19 17:06
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('kproperty', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='DynamicClause',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('prompt', models.CharField(editable=False, max_length=75)),
                ('category', models.CharField(choices=[('F', 'Financial'), ('D', 'Deadline'), ('U', 'Upkeep'), ('P', 'Possessions')], max_length=15)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('offer', models.FloatField()),
                ('deposit', models.FloatField()),
                ('comment', models.CharField(blank=True, max_length=350)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StaticClause',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('preview', models.TextField()),
                ('is_active', models.BooleanField(default=True, editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('buyer_accepted_offer', models.UUIDField(blank=True, null=True)),
                ('seller_accepted_offer', models.UUIDField(blank=True, null=True)),
                ('buyer_accepted_contract', models.UUIDField(blank=True, null=True)),
                ('seller_accepted_contract', models.UUIDField(blank=True, null=True)),
                ('stage', models.IntegerField(choices=[(0, 'OFFER_STAGE'), (1, 'NEGOTIATION_STAGE'), (2, 'CLOSING_STAGE')], default=0)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('buyer', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='buyer', to=settings.AUTH_USER_MODEL)),
                ('kproperty', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='kproperty', to='kproperty.Property')),
                ('seller', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='seller', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BuyerArrangesMortgageClause',
            fields=[
                ('dynamicclause_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='transaction.DynamicClause')),
                ('value', models.BooleanField(default=True)),
                ('ui_type', models.CharField(default='TOGGLE', editable=False, max_length=6)),
            ],
            options={
                'abstract': False,
            },
            bases=('transaction.dynamicclause',),
        ),
        migrations.CreateModel(
            name='ChattelsAndFixsClause',
            fields=[
                ('dynamicclause_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='transaction.DynamicClause')),
                ('value', models.BooleanField(default=True)),
                ('ui_type', models.CharField(default='TOGGLE', editable=False, max_length=6)),
            ],
            options={
                'abstract': False,
            },
            bases=('transaction.dynamicclause',),
        ),
        migrations.CreateModel(
            name='ChattelsIncludedClause',
            fields=[
                ('dynamicclause_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='transaction.DynamicClause')),
                ('value', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=15), default=list, size=None)),
                ('ui_type', models.CharField(default='CHIP', editable=False, max_length=10)),
            ],
            options={
                'abstract': False,
            },
            bases=('transaction.dynamicclause',),
        ),
        migrations.CreateModel(
            name='CompletionDateClause',
            fields=[
                ('dynamicclause_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='transaction.DynamicClause')),
                ('value', models.DateField(auto_now_add=True)),
                ('ui_type', models.CharField(default='DATE', editable=False, max_length=10)),
            ],
            options={
                'abstract': False,
            },
            bases=('transaction.dynamicclause',),
        ),
        migrations.CreateModel(
            name='CondoContract',
            fields=[
                ('contract_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='transaction.Contract')),
            ],
            bases=('transaction.contract',),
        ),
        migrations.CreateModel(
            name='CoOpContract',
            fields=[
                ('contract_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='transaction.Contract')),
            ],
            bases=('transaction.contract',),
        ),
        migrations.CreateModel(
            name='DepositClause',
            fields=[
                ('dynamicclause_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='transaction.DynamicClause')),
                ('ui_type', models.CharField(default='TEXT', editable=False, max_length=10)),
                ('value', models.PositiveIntegerField(null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('transaction.dynamicclause',),
        ),
        migrations.CreateModel(
            name='EnvironmentClause',
            fields=[
                ('dynamicclause_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='transaction.DynamicClause')),
                ('value', models.BooleanField(default=True)),
                ('ui_type', models.CharField(default='TOGGLE', editable=False, max_length=6)),
            ],
            options={
                'abstract': False,
            },
            bases=('transaction.dynamicclause',),
        ),
        migrations.CreateModel(
            name='EquipmentClause',
            fields=[
                ('dynamicclause_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='transaction.DynamicClause')),
                ('value', models.BooleanField(default=True)),
                ('ui_type', models.CharField(default='TOGGLE', editable=False, max_length=6)),
            ],
            options={
                'abstract': False,
            },
            bases=('transaction.dynamicclause',),
        ),
        migrations.CreateModel(
            name='FixturesExcludedClause',
            fields=[
                ('dynamicclause_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='transaction.DynamicClause')),
                ('value', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=15), default=list, size=None)),
                ('ui_type', models.CharField(default='CHIP', editable=False, max_length=10)),
            ],
            options={
                'abstract': False,
            },
            bases=('transaction.dynamicclause',),
        ),
        migrations.CreateModel(
            name='FreeholdContract',
            fields=[
                ('contract_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='transaction.Contract')),
            ],
            bases=('transaction.contract',),
        ),
        migrations.CreateModel(
            name='IrrevocabilityClause',
            fields=[
                ('dynamicclause_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='transaction.DynamicClause')),
                ('value', models.DateField(auto_now_add=True)),
                ('ui_type', models.CharField(default='DATE', editable=False, max_length=10)),
            ],
            options={
                'abstract': False,
            },
            bases=('transaction.dynamicclause',),
        ),
        migrations.CreateModel(
            name='MaintenanceClause',
            fields=[
                ('dynamicclause_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='transaction.DynamicClause')),
                ('value', models.BooleanField(default=True)),
                ('ui_type', models.CharField(default='TOGGLE', editable=False, max_length=6)),
            ],
            options={
                'abstract': False,
            },
            bases=('transaction.dynamicclause',),
        ),
        migrations.CreateModel(
            name='MobileContract',
            fields=[
                ('contract_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='transaction.Contract')),
            ],
            bases=('transaction.contract',),
        ),
        migrations.CreateModel(
            name='MortgageDeadlineClause',
            fields=[
                ('dynamicclause_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='transaction.DynamicClause')),
                ('value', models.DateField(auto_now_add=True)),
                ('ui_type', models.CharField(default='DATE', editable=False, max_length=10)),
            ],
            options={
                'abstract': False,
            },
            bases=('transaction.dynamicclause',),
        ),
        migrations.CreateModel(
            name='PaymentMethodClause',
            fields=[
                ('dynamicclause_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='transaction.DynamicClause')),
                ('options', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=15), size=None)),
                ('ui_type', models.CharField(default='DROPDOWN', editable=False, max_length=10)),
                ('value', models.CharField(blank=True, max_length=15, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('transaction.dynamicclause',),
        ),
        migrations.CreateModel(
            name='RentalItemsClause',
            fields=[
                ('dynamicclause_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='transaction.DynamicClause')),
                ('value', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=15), default=list, size=None)),
                ('ui_type', models.CharField(default='CHIP', editable=False, max_length=10)),
            ],
            options={
                'abstract': False,
            },
            bases=('transaction.dynamicclause',),
        ),
        migrations.CreateModel(
            name='SurveyDeadlineClause',
            fields=[
                ('dynamicclause_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='transaction.DynamicClause')),
                ('value', models.DateField(auto_now_add=True)),
                ('ui_type', models.CharField(default='DATE', editable=False, max_length=10)),
            ],
            options={
                'abstract': False,
            },
            bases=('transaction.dynamicclause',),
        ),
        migrations.CreateModel(
            name='UFFIClause',
            fields=[
                ('dynamicclause_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='transaction.DynamicClause')),
                ('value', models.BooleanField(default=True)),
                ('ui_type', models.CharField(default='TOGGLE', editable=False, max_length=6)),
            ],
            options={
                'abstract': False,
            },
            bases=('transaction.dynamicclause',),
        ),
        migrations.AddField(
            model_name='staticclause',
            name='contract',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='static_clauses', to='transaction.Contract'),
        ),
        migrations.AddField(
            model_name='offer',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offers', to='transaction.Transaction'),
        ),
        migrations.AddField(
            model_name='dynamicclause',
            name='_content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='dynamicclause',
            name='contract',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dynamic_clauses', to='transaction.Contract'),
        ),
        migrations.AddField(
            model_name='contract',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contracts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contract',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contracts', to='transaction.Transaction'),
        ),
        migrations.CreateModel(
            name='POTLFreeholdContract',
            fields=[
                ('freeholdcontract_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='transaction.FreeholdContract')),
            ],
            bases=('transaction.freeholdcontract',),
        ),
        migrations.AlterUniqueTogether(
            name='transaction',
            unique_together=set([('buyer', 'seller', 'kproperty')]),
        ),
    ]
