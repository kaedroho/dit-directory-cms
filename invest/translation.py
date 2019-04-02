from modeltranslation.decorators import register

from core.translation import BaseTranslationOptions
from . import models


@register(models.InvestHomePage)
class InvestHomePageTranslation(BaseTranslationOptions):
    fields = models.InvestHomePage.translatable_fields


@register(models.SectorPage)
class SectorPageTranslation(BaseTranslationOptions):
    fields = models.SectorPage.translatable_fields


@register(models.SectorLandingPage)
class SectorLandingPageTranslation(BaseTranslationOptions):
    fields = models.SectorLandingPage.translatable_fields


@register(models.RegionLandingPage)
class RegionLandingPageTranslation(BaseTranslationOptions):
    fields = models.RegionLandingPage.translatable_fields


@register(models.InfoPage)
class InfoPageTranslation(BaseTranslationOptions):
    fields = models.InfoPage.translatable_fields


@register(models.SetupGuidePage)
class SetupGuidePageTranslation(BaseTranslationOptions):
    fields = models.SetupGuidePage.translatable_fields


@register(models.SetupGuideLandingPage)
class SetupGuideLandingPageTranslation(BaseTranslationOptions):
    fields = models.SetupGuideLandingPage.translatable_fields


@register(models.HighPotentialOpportunityFormPage)
class HighPotentialOpportunityFormPageTranslationOptions(
    BaseTranslationOptions
):
    fields = []


@register(models.HighPotentialOpportunityDetailPage)
class HighPotentialOpportunityDetailPageTranslationOptions(
    BaseTranslationOptions
):
    fields = []


@register(models.InvestApp)
class InvestAppTranslationOptions(BaseTranslationOptions):
    fields = []


@register(models.HighPotentialOpportunityFormSuccessPage)
class HighPotentialOpportunityFormSuccessPageTranslationOptions(
    BaseTranslationOptions
):
    fields = []
