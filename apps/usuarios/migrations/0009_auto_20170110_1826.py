# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-10 18:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0008_auto_20170110_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='organizacion',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='puesto',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]