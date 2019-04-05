import copy
import os
from urllib.parse import urljoin

import bleach
import markdown

from bleach_whitelist import markdown_tags, markdown_attrs
from wagtail.admin.edit_handlers import ObjectList, TabbedInterface
from wagtail.core import hooks
from wagtail.core.models import Page
from wagtail.documents.models import Document
from wagtail.images.models import Image

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.images import get_image_dimensions
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from django.utils.translation import trans_real
from django.urls import resolve, Resolver404

from core import permissions


class CachedResponse(JsonResponse):
    pass


def make_translated_interface(
    content_panels, settings_panels=None, other_panels=None
):  # DELETEME
    panels = [ObjectList(
        content_panels,
        heading="Content"
    )]
    if settings_panels:
        panels.append(
            ObjectList(
                settings_panels, classname='settings', heading='Settings'
            )
        )
    if other_panels:
        panels += other_panels
    return TabbedInterface(panels)


def get_language_from_querystring(request):
    language_code = request.GET.get('lang')
    language_codes = trans_real.get_languages()
    if language_code and language_code in language_codes:
        return language_code


def get_or_create_document(document_path):
    document = default_storage.get_document_by_path(document_path)
    if not document:
        document_file = default_storage.open(document_path)
        document = Document.objects.create(
            title=os.path.basename(document_path),
            file=document_file,
        )
    return document


def get_or_create_image(image_path):
    image = default_storage.get_image_by_path(image_path)
    if not image:
        image_file = default_storage.open(image_path)
        width, height = get_image_dimensions(image_file)
        image = Image.objects.create(
            title=os.path.basename(image_path),
            width=width,
            height=height,
            file=image_path,
        )
    return image


def is_draft_requested(request):
    return permissions.DraftTokenPermisison.TOKEN_PARAM in request.GET


# from https://github.com/wagtail/wagtail/wagtail/tests/utils/form_data.py
def _nested_form_data(data):
    if isinstance(data, dict):
        items = data.items()
    elif isinstance(data, list):
        items = enumerate(data)

    for key, value in items:
        key = str(key)
        if isinstance(value, (dict, list)):
            for child_keys, child_value in _nested_form_data(value):
                yield [key] + child_keys, child_value
        else:
            yield [key], value


# from https://github.com/wagtail/wagtail/wagtail/tests/utils/form_data.py
def nested_form_data(data):
    return {'-'.join(key): value for key, value in _nested_form_data(data)}


# from https://github.com/wagtail/wagtail/wagtail/tests/utils/form_data.py
def inline_formset(items, initial=0, min=0, max=1000):
    def to_form(index, item):
        defaults = {
            'ORDER': str(index),
            'DELETE': '',
        }
        defaults.update(item)
        return defaults

    data_dict = {str(index): to_form(index, item)
                 for index, item in enumerate(items)}

    data_dict.update({
        'TOTAL_FORMS': str(len(data_dict)),
        'INITIAL_FORMS': str(initial),
        'MIN_NUM_FORMS': str(min),
        'MAX_NUM_FORMS': str(max),
    })
    return data_dict


def replace_hook(hook_name, original_fn):
    hooks._hooks[hook_name].remove((original_fn, 0))

    def inner(fn):
        hooks.register('register_page_listing_buttons', fn)
        return fn
    return inner


def get_button_url_name(button):
    try:
        return resolve(button.url).url_name
    except Resolver404:
        return None


def render_markdown(text, context=None):
    allowed_table_tags = ['table', 'thead', 'tbody', 'tfoot', 'tr', 'th', 'td']
    allowed_tags = markdown_tags+allowed_table_tags
    html = markdown.markdown(
        text,
        extensions=[
            'tables',
            'smarty',
            LinkerExtension()
        ],
        output_format='html5'
    )
    sanitised_html = bleach.clean(
        html,
        tags=allowed_tags,
        attributes=markdown_attrs,
    )
    return mark_safe(sanitised_html)


class LinkPattern(markdown.inlinepatterns.LinkPattern):
    def sanitize_url(self, url):
        #if url.startswith('slug:'):
        #    slug = url.split(':')[1]
        #    page = Page.objects.get(slug=slug).specific
        #    url = page.url
        return super().sanitize_url(url)


class LinkerExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns['link'] = LinkPattern(
            markdown.inlinepatterns.LINK_RE, md
        )


def get_page_full_url(domain, full_path):
    """ Urljoin quirkiness

    urljoin('http://great.gov.uk/international/', 'test/')
    http://great.gov.uk/international/test/

    urljoin('http://great.gov.uk/international', 'test/')
    http://great.gov.uk/test/

    urljoin('http://great.gov.uk/international/', '/test/')
    http://great.gov.uk/test/

    urljoin('http://great.gov.uk/international', '/test/')
    http://great.gov.uk/test/

    The first one is right!
    """

    if not domain.endswith('/'):
        domain = f'{domain}/'
    if full_path.startswith('/'):
        full_path = full_path[1:]
    url = urljoin(domain, full_path)
    return url
