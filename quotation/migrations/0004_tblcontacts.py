# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-17 19:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quotation', '0003_auto_20181117_1950'),
    ]

    operations = [
        migrations.CreateModel(
            name='tblContacts',
            fields=[
                ('Contactid_tblContacts', models.AutoField(primary_key=True, serialize=False)),
                ('firstname_tblcontacts', models.CharField(default='s', max_length=200)),
                ('lastname_tblcontacts', models.CharField(default='s', max_length=200)),
                ('Companyid_tblContacts', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tbl', to='quotation.tblCompanies')),
            ],
        ),
    ]
