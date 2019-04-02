from modeltranslation.decorators import register

from core.translation import BaseTranslationOptions
from find_a_supplier import models


@register(models.FindASupplierApp)
class FindASupplierAppTranslationOptions(BaseTranslationOptions):
    fields = []


@register(models.IndustryPage)
class IndustryPageTranslationOptions(BaseTranslationOptions):
    fields = models.IndustryPage.translatable_fields


@register(models.IndustryPageArticleSummary)
class IndustryPageArticleSummaryTranslationOptions(BaseTranslationOptions):
    fields = (
        'page',
    )


@register(models.IndustryArticlePage)
class IndustryArticlePageTranslationOptions(BaseTranslationOptions):
    fields = models.IndustryArticlePage.translatable_fields


@register(models.IndustryLandingPage)
class IndustryLandingPageTranslationOptions(BaseTranslationOptions):
    fields = models.IndustryLandingPage.translatable_fields


@register(models.LandingPage)
class LandingPageTranslationOptions(BaseTranslationOptions):
    fields = models.LandingPage.translatable_fields


@register(models.LandingPageArticleSummary)
class LandingPageArticleSummaryTranslationOptions(BaseTranslationOptions):
    fields = (
        'page',
    )


@register(models.IndustryContactPage)
class IndustryContactPageTranslationOptions(BaseTranslationOptions):
    fields = models.IndustryContactPage.translatable_fields
