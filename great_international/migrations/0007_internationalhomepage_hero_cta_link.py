# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-11 07:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('great_international', '0006_auto_20190325_0945'),
    ]

    operations = [
        migrations.AddField(
            model_name='internationalhomepage',
            name='hero_cta_link',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
