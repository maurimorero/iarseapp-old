# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-11 13:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0003_auto_20170106_2000'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dimension',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Encuesta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='dimension',
            name='encuesta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='survey.Encuesta'),
        ),
        migrations.AddField(
            model_name='survey',
            name='dimension',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='survey.Dimension'),
        ),
    ]
