# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-17 19:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quotation', '0004_tblcontacts'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbldoc',
            name='Contactid_tblDoc',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tblDoc_kinx', to='quotation.tblContacts'),
        ),
    ]
