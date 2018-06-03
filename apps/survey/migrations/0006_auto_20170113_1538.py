# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-13 15:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0005_auto_20170113_1535'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='responsemgr',
            name='survey',
        ),
        migrations.AddField(
            model_name='responsemgr',
            name='encuesta',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='survey.Encuesta'),
        ),
    ]