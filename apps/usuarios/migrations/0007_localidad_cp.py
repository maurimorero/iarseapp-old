# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-10 14:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0006_auto_20170110_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='localidad',
            name='cp',
            field=models.CharField(default=1, max_length=40),
        ),
    ]
