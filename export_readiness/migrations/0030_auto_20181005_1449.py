# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-05 14:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('export_readiness', '0029_auto_20181004_1003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepage',
            name='related_article_one_teaser',
            field=models.CharField(blank=True, help_text='Paste the article description here (max 255 characters)', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='articlepage',
            name='related_article_one_title',
            field=models.CharField(blank=True, help_text='Paste the title of the article here', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='articlepage',
            name='related_article_one_url',
            field=models.CharField(blank=True, help_text='Paste the article path here (eg /foo/bar/)', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='articlepage',
            name='related_article_three_teaser',
            field=models.CharField(blank=True, help_text='Paste the article description here (max 255 characters)', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='articlepage',
            name='related_article_three_title',
            field=models.CharField(blank=True, help_text='Paste the title of the article here', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='articlepage',
            name='related_article_three_url',
            field=models.CharField(blank=True, help_text='Paste the article path here (eg /foo/bar/)', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='articlepage',
            name='related_article_two_teaser',
            field=models.CharField(blank=True, help_text='Paste the article description here (max 255 characters)', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='articlepage',
            name='related_article_two_title',
            field=models.CharField(blank=True, help_text='Paste the title of the article here', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='articlepage',
            name='related_article_two_url',
            field=models.CharField(blank=True, help_text='Paste the article path here (eg /foo/bar/)', max_length=255, null=True),
        ),
    ]
