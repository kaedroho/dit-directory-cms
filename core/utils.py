from django.conf import settings

from wagtail_i18n.models import TranslatablePageMixin


def get_page_languages(page):
    if isinstance(page, TranslatablePageMixin):
        return page.get_translations(inclusive=True).values_list('locale__language__code', flat=True)
    else:
        return [settings.LANGUAGE_CODE]


def get_page_locales(page):
    if isinstance(page, TranslatablePageMixin):
        return page.get_translations(inclusive=True).values_list('locale__region__slug', 'locale__language__code')
    else:
        return [('default', settings.LANGUAGE_CODE)]


def get_page_language(page):
    if isinstance(page, TranslatablePageMixin):
        return page.locale.language.code
    else:
        return [settings.LANGUAGE_CODE]


def get_page_locale(page):
    if isinstance(page, TranslatablePageMixin):
        return page.locale.region.slug, page.locale.language.code
    else:
        return [('default', settings.LANGUAGE_CODE)]
