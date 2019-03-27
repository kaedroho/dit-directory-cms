# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-26 13:59
from __future__ import unicode_literals

from django.db import migrations

from wagtail_i18n.bootstrap import BootstrapTranslatableModel


class Migration(migrations.Migration):

    dependencies = [
        ('great_international', '0007_enable_wagtail_i18n_1'),
    ]

    operations = [
        BootstrapTranslatableModel('great_international.InternationalArticleListingPage'),
        BootstrapTranslatableModel('great_international.InternationalArticlePage'),
        BootstrapTranslatableModel('great_international.InternationalCampaignPage'),
        BootstrapTranslatableModel('great_international.InternationalCuratedTopicLandingPage'),
        BootstrapTranslatableModel('great_international.InternationalGuideLandingPage'),
        BootstrapTranslatableModel('great_international.InternationalSectorPage'),
        BootstrapTranslatableModel('great_international.InternationalTopicLandingPage'),
    ]