import itertools

from django import forms
from django.conf import settings

from wagtail.admin.forms import WagtailAdminPageForm


class CopyToEnvironmentForm(forms.Form):

    environment = forms.ChoiceField(
        label='Website',
        help_text='The website you would like to copy the page to',
        choices=[(url, url) for url in settings.COPY_DESTINATION_URLS]
    )


class WagtailAdminPageForm(WagtailAdminPageForm):

    @property
    def media(self):
        media = super().media
        media.add_js(['core/js/sum_required_localised_fields.js'])
        return media

    def __new__(cls, data=None, *args, **kwargs):
        form_class = super().__new__(cls)
        cls.set_read_only(form_class)
        return form_class

    def __init__(self, *args, **kwargs):
        """Set slug to read only if editing an existing page."""
        instance = kwargs.get('instance')
        if instance and instance.pk:
            field = self.base_fields.get('slug')  # App pages don't have slug
            if field:
                field.disabled = True
                field.required = False
        super().__init__(*args, **kwargs)

    @staticmethod
    def set_read_only(form_class):
        for field_name in form_class._meta.model.read_only_fields:
            if field_name in form_class.base_fields:
                field = form_class.base_fields[field_name]
                field.disabled = True
                field.required = False


class WagtailAdminPageExclusivePageForm(WagtailAdminPageForm):

    def __init__(self, *args, **kwargs):
        if 'initial' not in kwargs:
            kwargs['initial'] = {
                'slug': self._meta.model.slug_identity
            }
        super().__init__(*args, **kwargs)


class BaseAppAdminPageForm(WagtailAdminPageExclusivePageForm):
    pass
