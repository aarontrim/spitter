# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-05 09:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_spitt_time_pub'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spitt',
            name='time_pub',
            field=models.DateTimeField(default='2000-01-01'),
        ),
    ]
