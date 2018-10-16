# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-21 13:43
from __future__ import unicode_literals

import core.fields
import core.models
import core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
        ('export_readiness', '0001_squashed_0009_performancedashboardpage_guidance_notes'),
    ]

    operations = [
        migrations.CreateModel(
            name='PerformanceDashboardNotesPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', core.fields.MarkdownField(validators=[core.validators.slug_hyperlinks])),
            ],
            options={
                'abstract': False,
            },
            bases=(core.models.ExclusivePageMixin, 'wagtailcore.page'),
        ),
    ]
