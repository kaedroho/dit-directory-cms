# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-01-25 10:37
from __future__ import unicode_literals

import core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
        ('export_readiness', '0045_auto_20190115_1058'),
    ]

    operations = [
        migrations.CreateModel(
            name='EUExitFormPages',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('service_name', models.CharField(choices=[('FIND_A_SUPPLIER', 'Find a Supplier'), ('EXPORT_READINESS', 'Export Readiness'), ('INVEST', 'Invest'), ('COMPONENTS', 'Components')], db_index=True, max_length=100, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(core.models.ExclusivePageMixin, 'wagtailcore.page'),
        ),
    ]
