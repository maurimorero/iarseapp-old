# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-05 13:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0012_auto_20170203_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(default='', max_length=254),
        ),
    ]