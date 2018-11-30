import pytest
from rest_framework.serializers import Serializer

from django.utils import translation

from core import api_serializers, permissions
from invest.tests.factories import HighPotentialOpportunityFormPageFactory
from find_a_supplier.tests.factories import (
    IndustryLandingPageFactory,
    IndustryPageFactory,
    LandingPageFactory,
    IndustryContactPageFactory,
)


@pytest.mark.django_db
def test_markdown_to_html_serializer(page, rf):
    page.hero_text_en_gb = (
        '[hyperlink](slug:{slug})'.format(slug=page.slug)
    )

    class TestSerializer(Serializer):
        hero_text_en_gb = api_serializers.APIMarkdownToHTMLSerializer()

    serializer = TestSerializer(
        instance=page,
        context={'request': rf.get('/')}
    )

    assert serializer.data == {
        'hero_text_en_gb': (
            '<p><a href="http://supplier.trade.great:8005/'
            'industries/the-slug/">hyperlink</a></p>'
        )
    }


@pytest.mark.django_db
def test_meta_serializer(page, rf):
    page.slug = 'test-slug'
    page.pk = 4

    class TestSerializer(Serializer):
        meta = api_serializers.APIMetaSerializer()

    serializer = TestSerializer(
        instance=page,
        context={'request': rf.get('/')}
    )

    assert serializer.data == {
        'meta': {
            'draft_token': None,
            'languages': [('en-gb', 'English')],
            'url': 'http://supplier.trade.great:8005/industries/test-slug/',
            'localised_urls': [
                (
                    'en-gb',
                    'http://supplier.trade.great:8005/industries/test-slug/'
                )
            ],
            'slug': 'test-slug',
            'pk': page.pk
        }
    }


@pytest.mark.django_db
def test_meta_serializer_slug_translation(page, rf):
    page.slug = 'test-slug-en'
    page.pk = 4

    class TestSerializer(Serializer):
        meta = api_serializers.APIMetaSerializer()

    with translation.override('de'):
        serializer = TestSerializer(
            instance=page,
            context={'request': rf.get('/')}
        )
        data = serializer.data

    assert data == {
        'meta': {
            'draft_token': None,
            'languages': [('en-gb', 'English')],
            'url': 'http://supplier.trade.great:8005/industries/test-slug-en/',
            'localised_urls': [
                (
                    'en-gb',
                    'http://supplier.trade.great:8005/industries/test-slug-en/'
                )
            ],
            'slug': 'test-slug-en',
            'pk': page.pk,
        }
    }


@pytest.mark.django_db
def test_meta_serializer_contains_draft_token(page_with_reversion, rf):
    page_with_reversion.slug = 'test-slug'
    page_with_reversion.pk = 4

    class TestSerializer(Serializer):
        meta = api_serializers.APIMetaSerializer()

    serializer = TestSerializer(
        instance=page_with_reversion,
        context={'request': rf.get('/')}
    )

    url = 'http://supplier.trade.great:8005/industries/test-slug/'
    assert serializer.data == {
        'meta': {
            'draft_token': page_with_reversion.get_draft_token(),
            'languages': [
                ('en-gb', 'English'), ('de', 'Deutsch'), ('ja', '日本語'),
                ('ru', 'Russian'), ('zh-hans', '简体中文'), ('fr', 'Français'),
                ('es', 'español'), ('pt', 'Português'),
                ('pt-br', 'Português Brasileiro'), ('ar', 'العربيّة'),
            ],
            'url': url,
            'localised_urls': [
                ('en-gb', url),
                ('de', '{}{}'.format(url, '?lang=de')),
                ('ja', '{}{}'.format(url, '?lang=ja')),
                ('ru', '{}{}'.format(url, '?lang=ru')),
                ('zh-hans', '{}{}'.format(url, '?lang=zh-hans')),
                ('fr', '{}{}'.format(url, '?lang=fr')),
                ('es', '{}{}'.format(url, '?lang=es')),
                ('pt', '{}{}'.format(url, '?lang=pt')),
                ('pt-br', '{}{}'.format(url, '?lang=pt-br')),
                ('ar', '{}{}'.format(url, '?lang=ar'))
            ],
            'slug': 'test-slug',
            'pk': page_with_reversion.pk,
        }
    }


@pytest.mark.django_db
def test_meta_serializer_draft(page, rf):

    class TestSerializer(Serializer):
        meta = api_serializers.APIMetaSerializer()

    request = rf.get('/', {permissions.DraftTokenPermisison.TOKEN_PARAM: '1'})
    serializer = TestSerializer(instance=page, context={'request': request})

    assert serializer.data['meta']['url'] == page.get_url(is_draft=True)


@pytest.mark.django_db
def test_breadcrums_serializer(page, rf):
    IndustryLandingPageFactory(breadcrumbs_label_en_gb='label-one')
    IndustryPageFactory(breadcrumbs_label_en_gb='label-two')
    LandingPageFactory(breadcrumbs_label_en_gb='label-three')
    IndustryContactPageFactory(breadcrumbs_label_en_gb='label-four')

    class TestSerializer(Serializer):
        breadcrumbs = api_serializers.APIBreadcrumbsSerializer(
            service_name='FIND_A_SUPPLIER'
        )

    serializer = TestSerializer(
        instance=page,
        context={'request': rf.get('/')}
    )

    assert serializer.data == {
        'breadcrumbs': {
            'industrylandingpage': {
                'slug': 'industries-landing-page',
                'label': 'label-one'
            },
            'industrycontactpage': {
                'slug': 'industry-contact',
                'label': 'label-four'
            },
            'landingpage': {
                'slug': 'landing-page',
                'label': 'label-three'
            }
        }
    }


@pytest.mark.django_db
def test_api_form_field_serializer(rf):
    page = HighPotentialOpportunityFormPageFactory(
        comment_help_text='comment [help text]',
        comment_label='comment [label]',
        breadcrumbs_label='HPO form',
    )

    class TestSerializer(Serializer):
        comment = api_serializers.APIFormFieldSerializer('comment')

    serializer = TestSerializer(
        instance=page,
        context={'request': rf.get('/')}
    )

    assert serializer.data == {
        'comment': {
            'help_text': 'comment [help text]',
            'label': 'comment [label]',
        }
    }