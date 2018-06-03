# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-05 13:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuarios', '0013_auto_20170205_1332'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('survey', '0019_remove_responsemgr_provincia'),
    ]

    operations = [
        migrations.CreateModel(
            name='Indicador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('nota', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='IndicadorMgr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('rspMgr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.ResponseMgr')),
                ('ubicacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.Provincia')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TipoIndicador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('description', models.TextField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='indicador',
            name='indMgr',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='indicadores.IndicadorMgr'),
        ),
        migrations.AddField(
            model_name='indicador',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='indicadores.TipoIndicador'),
        ),
    ]
