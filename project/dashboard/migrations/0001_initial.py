# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-15 00:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('ip', models.GenericIPAddressField(protocol='IPv4', unique=True)),
            ],
        ),
    ]
