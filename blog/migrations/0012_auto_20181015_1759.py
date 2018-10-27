# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-15 15:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_doc_details_product_description_tbldoc_details'),
    ]

    operations = [
        migrations.CreateModel(
            name='tblDoc_details',
            fields=[
                ('Doc_detailsid_tblDoc_details', models.AutoField(primary_key=True, serialize=False)),
                ('Qty_tblDoc_details', models.IntegerField(default=1)),
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
        migrations.RenameModel(
            old_name='Doc',
            new_name='tblDoc',
        ),
        migrations.RemoveField(
            model_name='doc_details',
            name='Docid_tblDoc_details',
        ),
        migrations.DeleteModel(
            name='Doc_details',
        ),
        migrations.AddField(
            model_name='tbldoc_details',
            name='Docid_tblDoc_details',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tblDoc', to='blog.tblDoc'),
        ),
        migrations.AddField(
            model_name='tbldoc_details',
            name='Productid_tblDoc_details',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tblProduct', to='blog.tblProduct'),
        ),
    ]
