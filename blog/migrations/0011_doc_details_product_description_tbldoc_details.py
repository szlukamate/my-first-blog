# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-11 14:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20181011_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='doc_details',
            name='Product_description_tblDoc_details',
            field=models.CharField(default='Something', max_length=200),
        ),
    ]
