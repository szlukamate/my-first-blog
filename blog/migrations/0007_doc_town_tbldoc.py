# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-11 10:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20181010_1820'),
    ]

    operations = [
        migrations.AddField(
            model_name='doc',
            name='Town_tblDoc',
            field=models.CharField(default='Szeged', max_length=200),
        ),
    ]