# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-09 20:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indicadores', '0003_indicador_orden'),
    ]

    operations = [
        migrations.AddField(
            model_name='nota',
            name='orden',
            field=models.IntegerField(default=1, null=True),
        ),
    ]