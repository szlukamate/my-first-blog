# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-17 13:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='tblDoc',
            fields=[
                ('Docid_tblDoc', models.AutoField(primary_key=True, serialize=False)),
                ('Pcd_tblDoc', models.CharField(max_length=201)),
                ('Town_tblDoc', models.CharField(default='Szeged', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='tblDoc_details',
            fields=[
                ('Doc_detailsid_tblDoc_details', models.AutoField(primary_key=True, serialize=False)),
                ('Qty_tblDoc_details', models.IntegerField(default=1)),
                ('firstnum_tblDoc_details', models.IntegerField(default=1)),
                ('secondnum_tblDoc_details', models.IntegerField(default=0)),
                ('thirdnum_tblDoc_details', models.IntegerField(default=0)),
                ('fourthnum_tblDoc_details', models.IntegerField(default=0)),
                ('Note_tblDoc_details', models.CharField(default='Defaultnote', max_length=200)),
                ('Docid_tblDoc_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tblDoc', to='quotation.tblDoc')),
            ],
        ),
        migrations.CreateModel(
            name='tblDoc_kind',
            fields=[
                ('Doc_kindid_tblDoc_kind', models.AutoField(primary_key=True, serialize=False)),
                ('Doc_kind_name_tblDoc_kind', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='tblProduct',
            fields=[
                ('Productid_tblProduct', models.AutoField(primary_key=True, serialize=False)),
                ('Product_price_tblProduct', models.IntegerField(default=1)),
                ('Product_description_tblProduct', models.CharField(default='Something', max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='tbldoc_details',
            name='Productid_tblDoc_details',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tblProduct', to='quotation.tblProduct'),
        ),
        migrations.AddField(
            model_name='tbldoc',
            name='Doc_kindid_tblDoc',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tblDoc_kin', to='quotation.tblDoc_kind'),
        ),
    ]
