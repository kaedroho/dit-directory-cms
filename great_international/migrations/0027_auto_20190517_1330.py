# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-17 13:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('great_international', '0026_capitalinvestsectorrelatedpagesummary'),
    ]

    operations = [
        migrations.RenameField(
            model_name='capitalinvestsectorrelatedpagesummary',
            old_name='added_related_pages',
            new_name='related_opportunity_page',
        ),
    ]
