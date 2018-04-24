# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-10 11:09
from __future__ import unicode_literals

import core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
        ('export_readiness', '0002_auto_20180410_1038'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExportReadinessApp',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=(core.models.ExclusivePageMixin, 'wagtailcore.page'),
        ),
    ]