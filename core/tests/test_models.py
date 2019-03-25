import pytest

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import translation
from wagtail.core.models import Page

from find_a_supplier.tests.factories import IndustryPageFactory
from invest.tests.factories import InvestAppFactory, \
    SectorLandingPageFactory, SectorPageFactory
from invest.models import InvestApp


@pytest.mark.django_db
def test_slugs_are_unique_in_the_same_service():
    IndustryPageFactory(slug='foo')
    with pytest.raises(ValidationError) as excinfo:
        IndustryPageFactory(slug='foo')
    assert 'This slug is already in use' in str(excinfo.value)


@pytest.mark.django_db
def test_slugs_are_not_unique_across_services(root_page):
    page_one = IndustryPageFactory(slug='foo', parent=root_page)
    page_two = SectorPageFactory(slug='foo', parent=root_page)
    assert page_one.slug == 'foo'
    assert page_two.slug == 'foo'


@pytest.mark.django_db
def test_delete_same_slug_different_services(root_page):
    """
    Deleting a page results in ancestor pages being re-saved.
    Thus ancestor page (root_page) has to have title & title.
    """
    root_page.title = 'ancestor page has to have a title'
    root_page.save()
    page_one = IndustryPageFactory(slug='foo', parent=root_page)
    page_two = SectorPageFactory(slug='foo', parent=root_page)
    assert page_one.slug == 'foo'
    assert page_two.slug == 'foo'
    page_one.delete()
    assert Page.objects.filter(pk=page_one.pk).exists() is False


@pytest.mark.django_db
def test_page_path(root_page):
    page_one = SectorLandingPageFactory(parent=root_page)
    page_two = SectorPageFactory(slug='foo', parent=page_one)
    page_three = SectorPageFactory(slug='bar', parent=page_two)

    assert page_three.full_path == '/industries/foo/bar/'
    assert page_two.full_path == '/industries/foo/'


@pytest.mark.django_db
def test_base_model_check_valid_draft_token(page):
    draft_token = page.get_draft_token()

    assert page.is_draft_token_valid(draft_token) is True


@pytest.mark.django_db
def test_base_model_check_invalid_draft_token(page):
    assert page.is_draft_token_valid('asdf') is False


@pytest.mark.django_db
def test_base_model_sets_service_name_on_save(page):
    assert page.service_name == page.service_name_value


@pytest.mark.django_db
def test_base_model_redirect_published_url(rf, page):
    request = rf.get('/')

    response = page.serve(request)

    assert response.status_code == 302
    assert response.url == page.get_url()


@pytest.mark.django_db
def test_base_app_slugs_are_created_in_all_languages(root_page):
    app = InvestAppFactory(title='foo', parent=root_page)
    assert app.slug == InvestApp.slug_identity
