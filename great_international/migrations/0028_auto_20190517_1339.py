# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-17 13:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('great_international', '0027_auto_20190517_1330'),
    ]

    operations = [
        migrations.RenameField(
            model_name='capitalinvestsectorrelatedpagesummary',
            old_name='related_opportunity_page',
            new_name='added_related_pages',
        ),
    ]
