# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-17 18:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='tblCompanies',
            fields=[
                ('Companyid_tblCompanies', models.AutoField(primary_key=True, serialize=False)),
                ('companyname_tblcompanies', models.CharField(default='s', max_length=200)),
            ],
        ),
    ]
