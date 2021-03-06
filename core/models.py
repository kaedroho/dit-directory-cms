from functools import partial, reduce
import hashlib
from urllib.parse import urljoin, urlencode

from directory_constants.constants import choices
from django.core.exceptions import ValidationError
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.core.models import Page, PageBase

from django.core import signing
from django.conf import settings
from django.contrib.contenttypes.fields import (
    GenericForeignKey, GenericRelation
)
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db import transaction
from django.forms import MultipleChoiceField
from django.shortcuts import redirect
from django.utils import translation

from core import constants, forms
from core.helpers import get_page_full_url
from core.wagtail_fields import FormHelpTextField, FormLabelField


class Breadcrumb(models.Model):
    service_name = models.CharField(
        max_length=50,
        choices=choices.CMS_APP_CHOICES,
        null=True,
        db_index=True
    )
    label = models.CharField(max_length=50)
    slug = models.SlugField()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    page = GenericForeignKey('content_type', 'object_id')


class ChoiceArrayField(ArrayField):

    def formfield(self, **kwargs):
        defaults = {
            'form_class': MultipleChoiceField,
            'choices': self.base_field.choices,
        }
        defaults.update(kwargs)
        return super(ArrayField, self).formfield(**defaults)


class BasePage(Page):
    service_name = models.CharField(
        max_length=100,
        choices=choices.CMS_APP_CHOICES,
        db_index=True,
        null=True,
    )

    class Meta:
        abstract = True

    view_path = ''
    subpage_types = []
    base_form_class = forms.WagtailAdminPageForm
    content_panels = []
    promote_panels = []
    read_only_fields = []

    def __init__(self, *args, **kwargs):
        self.signer = signing.Signer()
        super().__init__(*args, **kwargs)

    @transaction.atomic
    def save(self, *args, **kwargs):
        self.service_name = self.service_name_value
        #if not self._slug_is_available(
        #    slug=self.slug,
        #    parent=self.get_parent(),
        #    page=self
        #):
        #    raise ValidationError({'slug': 'This slug is already in use'})
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """We need to override delete to use the Page's parent one.

        Using the Page one would cause the original _slug_is_available method
        to be called and that is not considering services
        """
        super(Page, self).delete(*args, **kwargs)

    #@staticmethod
    #def _slug_is_available(slug, parent, page=None):
    #    from core import filters  # circular dependencies
    #    queryset = filters.ServiceNameFilter().filter_service_name(
    #        queryset=Page.objects.filter(slug=slug).exclude(pk=page.pk),
    #        name=None,
    #        value=page.service_name,
    #    )
    #    is_unique_in_service = (queryset.count() == 0)
    #    return is_unique_in_service

    def get_draft_token(self):
        return self.signer.sign(self.pk)

    def is_draft_token_valid(self, draft_token):
        try:
            value = self.signer.unsign(draft_token)
        except signing.BadSignature:
            return False
        else:
            return str(self.pk) == str(value)

    def get_url_path_parts(self):
        return [self.view_path, self.slug + '/']

    def get_url(self, is_draft=False):
        domain = dict(constants.APP_URLS)[self.service_name_value]
        url_path_parts = self.get_url_path_parts()
        url = reduce(urljoin, [domain] + url_path_parts)
        querystring = {}
        if is_draft:
            querystring['draft_token'] = self.get_draft_token()
        if querystring:
            url += '?' + urlencode(querystring)
        return url

    @property
    def full_path(self):
        """Return the full path of a page, ignoring the root_page and
        the app page. Used by the lookup-by-url view in prototype mode
        """
        # starts from 2 to remove root page and app page
        path_components = [page.slug for page in self.get_ancestors()[2:]]
        path_components.append(self.slug)
        # need to also take into account the view_path if it's set
        if self.view_path:
            path_components.insert(0, self.view_path.replace('/', ''))
        return '/{path}/'.format(path='/'.join(path_components))

    @property
    def full_url(self):
        domain = dict(constants.APP_URLS)[self.service_name_value]
        return get_page_full_url(domain, self.full_path)

    @property
    def url(self):
        return self.get_url()

    def serve(self, request, *args, **kwargs):
        return redirect(self.get_url())

    def get_latest_nested_revision_as_page(self):
        revision = self.get_latest_revision_as_page()
        foreign_key_names = [
            field.name for field in revision._meta.get_fields()
            if isinstance(field, models.ForeignKey)
        ]
        for name in foreign_key_names:
            field = getattr(revision, name)
            if hasattr(field, 'get_latest_revision_as_page'):
                setattr(revision, name, field.get_latest_revision_as_page())
        return revision

    @classmethod
    def can_exist_under(cls, parent):
        if not parent.specific_class:
            return []
        return super().can_exist_under(parent)


class AbstractObjectHash(models.Model):
    class Meta:
        abstract = True

    content_hash = models.CharField(max_length=1000)

    @staticmethod
    def generate_content_hash(field_file):
        filehash = hashlib.md5()
        field_file.open()
        filehash.update(field_file.read())
        field_file.close()
        return filehash.hexdigest()


class DocumentHash(AbstractObjectHash):
    document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='+'
    )


class ImageHash(AbstractObjectHash):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='+'
    )


class ExclusivePageMixin:
    read_only_fields = ['slug']
    base_form_class = forms.WagtailAdminPageExclusivePageForm

    @classmethod
    def can_create_at(cls, parent):
        return super().can_create_at(parent) and not cls.objects.exists()

    def save(self, *args, **kwargs):
        if not self.pk and hasattr(self, 'slug_identity'):
            self.slug = self.slug_identity
        super().save(*args, **kwargs)

    def get_url_path_parts(self, *args, **kwargs):
        return [self.view_path]


class BreadcrumbMixin(models.Model):
    """Optimization for retrieving breadcrumbs that a service will display
    on a global navigation menu e.g., home > industry > contact us. Reduces SQL
    calls from >12 to 1 in APIBreadcrumbsSerializer compared with filtering
    Page and calling `specific()` and then retrieving the breadcrumbs labels.
    """

    class Meta:
        abstract = True

    breadcrumb = GenericRelation(Breadcrumb)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        defaults = {
            'service_name': self.service_name_value,
            'slug': self.slug,
        }
        defaults['label'] = self.breadcrumbs_label
        self.breadcrumb.update_or_create(defaults=defaults)


class ServiceMixin(models.Model):
    service_name_value = None
    base_form_class = forms.BaseAppAdminPageForm
    view_path = ''
    parent_page_types = ['wagtailcore.Page']

    class Meta:
        abstract = True

    @classmethod
    def allowed_subpage_models(cls):
        allowed_name = cls.service_name_value
        return [
            model for model in Page.allowed_subpage_models()
            if getattr(model, 'service_name_value', None) == allowed_name
        ]

    settings_panels = [
        FieldPanel('title')
    ]
    content_panels = []
    promote_panels = []


class FormPageMetaClass(PageBase):
    """Metaclass that adds <field_name>_label and <field_name>_help_text to a
    Page when given a list of form_field_names.
    """
    def __new__(mcls, name, bases, attrs):
        form_field_names = attrs['form_field_names']
        for field_name in form_field_names:
            attrs[field_name + '_help_text'] = FormHelpTextField()
            attrs[field_name + '_label'] = FormLabelField()

        form_panels = [
            MultiFieldPanel(
                heading=name.replace('_', ' '),
                children=[
                    FieldPanel(name + '_label'),
                    FieldPanel(name + '_help_text'),
                ]
            ) for name in form_field_names
        ]
        attrs['content_panels'] = (
            attrs['content_panels_before_form'] +
            form_panels +
            attrs['content_panels_after_form']
        )

        return super().__new__(mcls, name, bases, attrs)
