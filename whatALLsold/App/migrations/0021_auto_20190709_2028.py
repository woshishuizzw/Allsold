# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-07-09 12:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0020_flow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flow',
            name='ftime',
            field=models.DateField(),
        ),
    ]
