# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-19 17:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0011_auto_20170119_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='description',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]