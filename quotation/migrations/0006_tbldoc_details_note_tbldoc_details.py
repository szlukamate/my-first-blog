# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-29 21:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotation', '0005_auto_20181029_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbldoc_details',
            name='Note_tblDoc_details',
            field=models.CharField(default='Defaultnote', max_length=200),
        ),
    ]
