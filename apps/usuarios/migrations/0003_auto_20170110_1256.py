# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-10 12:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_auto_20170109_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='tipo',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]