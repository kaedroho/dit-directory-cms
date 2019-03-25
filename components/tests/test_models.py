import pytest

from components import models


def test_app_models():
    assert models.ComponentsApp.allowed_subpage_models() == [
        models.ComponentsApp,
        models.BannerComponent,
    ]


@pytest.mark.django_db
def test_set_slug():
    instance = models.ComponentsApp.objects.create(
        title='the app',
        depth=2,
        path='/thing',
    )

    assert instance.slug == models.ComponentsApp.slug_identity
