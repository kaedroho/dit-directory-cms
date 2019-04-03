from itertools import product

import pytest
from wagtail.documents.models import Document

from find_a_supplier.tests.factories import (
    IndustryPageFactory,
    IndustryLandingPageFactory
)
from invest.tests.factories import HighPotentialOpportunityDetailPageFactory


@pytest.fixture
def page(root_page):
    return IndustryPageFactory(
        parent=root_page,
        slug='the-slug'
    )


@pytest.fixture
def high_potential_opportunity_page(page):
    pdf_document = Document.objects.create(
        title='document.pdf',
        file=page.introduction_column_two_icon.file  # not really pdf
    )
    return HighPotentialOpportunityDetailPageFactory(pdf_document=pdf_document)


@pytest.fixture
def translated_page(settings, root_page):
    page = IndustryPageFactory(
        parent=root_page,
        title='title',
        breadcrumbs_label='label',
        introduction_text='lede',
        search_description='description',
        hero_text='hero text',
        introduction_column_one_text='lede column one',
        introduction_column_two_text='lede column two',
        introduction_column_three_text='lede column three',
        company_list_call_to_action_text='view all',
        company_list_text='the title',
        search_filter_sector=['FOOD_AND_DRINK'],
    )
    page.save()
    return page


@pytest.fixture
def fas_industry_landing_page(root_page):
    return IndustryLandingPageFactory(parent=root_page)


@pytest.fixture
def translated_fas_industry_page(settings, fas_industry_landing_page):
    page = IndustryPageFactory(
        parent=fas_industry_landing_page,
        title='title',
        breadcrumbs_label='label',
        introduction_text='lede',
        search_description='description',
        hero_text='hero text',
        introduction_column_one_text='lede column one',
        introduction_column_two_text='lede column two',
        introduction_column_three_text='lede column three',
        company_list_call_to_action_text='view all',
        company_list_text='the title',
        search_filter_sector=['FOOD_AND_DRINK'],
    )
    page.save()
    return page


@pytest.fixture
def page_with_reversion(admin_user, translated_page):
    translated_page.title = 'published-title',
    translated_page.title = 'published-title'
    translated_page.save()

    translated_page.title = 'draft-title'
    translated_page.save_revision(
        user=admin_user,
        submitted_for_moderation=False,
    )
    return translated_page
