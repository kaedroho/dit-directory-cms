# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-03 08:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0021_image_file_hash'),
        ('invest', '0026_auto_20190425_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='investhomepage',
            name='capital_invest_section_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='investhomepage',
            name='capital_invest_section_image_ar',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='investhomepage',
            name='capital_invest_section_image_de',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='investhomepage',
            name='capital_invest_section_image_en_gb',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='investhomepage',
            name='capital_invest_section_image_es',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='investhomepage',
            name='capital_invest_section_image_fr',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='investhomepage',
            name='capital_invest_section_image_ja',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='investhomepage',
            name='capital_invest_section_image_pt',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AddField(
            model_name='investhomepage',
            name='capital_invest_section_image_zh_hans',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AlterField(
            model_name='investhomepage',
            name='setup_guide_call_to_action_text',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='investhomepage',
            name='setup_guide_call_to_action_text_ar',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='investhomepage',
            name='setup_guide_call_to_action_text_de',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='investhomepage',
            name='setup_guide_call_to_action_text_en_gb',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='investhomepage',
            name='setup_guide_call_to_action_text_es',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='investhomepage',
            name='setup_guide_call_to_action_text_fr',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='investhomepage',
            name='setup_guide_call_to_action_text_ja',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='investhomepage',
            name='setup_guide_call_to_action_text_pt',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='investhomepage',
            name='setup_guide_call_to_action_text_zh_hans',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
