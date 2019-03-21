# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-03-21 08:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0021_image_file_hash'),
        ('great_international', '0008_auto_20190320_0910'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='internationalhomepage',
            name='invest_url',
        ),
        migrations.RemoveField(
            model_name='internationalhomepage',
            name='trade_url',
        ),
        migrations.AddField(
            model_name='internationalhomepage',
            name='hero_cta_text',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='internationalhomepage',
            name='hero_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='internationalhomepage',
            name='hero_title',
            field=models.CharField(default='The UK welcomes international businesses', max_length=255),
            preserve_default=False,
        ),
    ]
