# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-25 13:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0002_auto_20190206_1355'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bannercomponent',
            name='banner_content_ar',
        ),
        migrations.RemoveField(
            model_name='bannercomponent',
            name='banner_content_de',
        ),
        migrations.RemoveField(
            model_name='bannercomponent',
            name='banner_content_en_gb',
        ),
        migrations.RemoveField(
            model_name='bannercomponent',
            name='banner_content_es',
        ),
        migrations.RemoveField(
            model_name='bannercomponent',
            name='banner_content_fr',
        ),
        migrations.RemoveField(
            model_name='bannercomponent',
            name='banner_content_ja',
        ),
        migrations.RemoveField(
            model_name='bannercomponent',
            name='banner_content_pt',
        ),
        migrations.RemoveField(
            model_name='bannercomponent',
            name='banner_content_pt_br',
        ),
        migrations.RemoveField(
            model_name='bannercomponent',
            name='banner_content_ru',
        ),
        migrations.RemoveField(
            model_name='bannercomponent',
            name='banner_content_zh_hans',
        ),
        migrations.RemoveField(
            model_name='bannercomponent',
            name='banner_label_ar',
        ),
        migrations.RemoveField(
            model_name='bannercomponent',
            name='banner_label_de',
        ),
        migrations.RemoveField(
            model_name='bannercomponent',
            name='banner_label_en_gb',
        ),
        migrations.RemoveField(
            model_name='bannercomponent',
            name='banner_label_es',
        ),
        migrations.RemoveField(
            model_name='bannercomponent',
            name='banner_label_fr',
        ),
        migrations.RemoveField(
            model_name='bannercomponent',
            name='banner_label_ja',
        ),
        migrations.RemoveField(
            model_name='bannercomponent',
            name='banner_label_pt',
        ),
        migrations.RemoveField(
            model_name='bannercomponent',
            name='banner_label_pt_br',
        ),
        migrations.RemoveField(
            model_name='bannercomponent',
            name='banner_label_ru',
        ),
        migrations.RemoveField(
            model_name='bannercomponent',
            name='banner_label_zh_hans',
        ),
    ]
