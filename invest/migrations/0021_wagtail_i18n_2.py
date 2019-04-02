# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-02 15:44
from __future__ import unicode_literals

from django.db import migrations

from wagtail_i18n.bootstrap import BootstrapTranslatableModel


class Migration(migrations.Migration):

    dependencies = [
        ('invest', '0020_wagtail_i18n_1'),
    ]

    operations = [
        BootstrapTranslatableModel('invest.HighPotentialOpportunityDetailPage'),
        BootstrapTranslatableModel('invest.HighPotentialOpportunityFormPage'),
        BootstrapTranslatableModel('invest.HighPotentialOpportunityFormSuccessPage'),
        BootstrapTranslatableModel('invest.InfoPage'),
        BootstrapTranslatableModel('invest.InvestHomePage'),
        BootstrapTranslatableModel('invest.RegionLandingPage'),
        BootstrapTranslatableModel('invest.SectorLandingPage'),
        BootstrapTranslatableModel('invest.SectorPage'),
        BootstrapTranslatableModel('invest.SetupGuideLandingPage'),
        BootstrapTranslatableModel('invest.SetupGuidePage'),
    ]
