import itertools

import pytest


@pytest.mark.django_db
def test_slug_read_only_when_editing_a_page(translated_page, rf):

    edit_handler = translated_page.get_edit_handler()
    form_class = edit_handler.get_form_class()
    form = form_class(instance=translated_page)
    edit_handler.bind_to_instance(
        instance=translated_page,
        form=form,
        request=rf
    )

    assert form.fields['slug'].required is False
    assert form.fields['slug'].disabled is True


@pytest.mark.django_db
def test_slug_editable_when_creating_a_page(translated_page, rf):

    edit_handler = translated_page.get_edit_handler()
    form_class = edit_handler.get_form_class()
    form = form_class()
    edit_handler.bind_to_instance(
        instance=translated_page,
        form=form,
        request=rf
    )

    assert form.fields['slug'].required is True
    assert form.fields['slug'].disabled is False
