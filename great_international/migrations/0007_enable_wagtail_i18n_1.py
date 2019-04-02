# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-26 13:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtail_i18n', '__latest__'),
        ('great_international', '0006_auto_20190326_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='internationalarticlelistingpage',
            name='locale',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtail_i18n.Locale'),
        ),
        migrations.AddField(
            model_name='internationalarticlelistingpage',
            name='translation_key',
            field=models.UUIDField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='internationalarticlepage',
            name='locale',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtail_i18n.Locale'),
        ),
        migrations.AddField(
            model_name='internationalarticlepage',
            name='translation_key',
            field=models.UUIDField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='internationalcampaignpage',
            name='locale',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtail_i18n.Locale'),
        ),
        migrations.AddField(
            model_name='internationalcampaignpage',
            name='translation_key',
            field=models.UUIDField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='internationalcuratedtopiclandingpage',
            name='locale',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtail_i18n.Locale'),
        ),
        migrations.AddField(
            model_name='internationalcuratedtopiclandingpage',
            name='translation_key',
            field=models.UUIDField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='internationalguidelandingpage',
            name='locale',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtail_i18n.Locale'),
        ),
        migrations.AddField(
            model_name='internationalguidelandingpage',
            name='translation_key',
            field=models.UUIDField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='internationalsectorpage',
            name='locale',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtail_i18n.Locale'),
        ),
        migrations.AddField(
            model_name='internationalsectorpage',
            name='translation_key',
            field=models.UUIDField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='internationaltopiclandingpage',
            name='locale',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtail_i18n.Locale'),
        ),
        migrations.AddField(
            model_name='internationaltopiclandingpage',
            name='translation_key',
            field=models.UUIDField(editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='internationallocalerootpage',
            name='locale',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wagtail_i18n.Locale'),
        ),
    ]
