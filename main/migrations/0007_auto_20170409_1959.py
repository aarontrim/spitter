# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-09 09:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20170408_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='biography',
            field=models.CharField(default='My bio here...', max_length=300),
        ),
    ]
