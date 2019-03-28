import markdown
from bs4 import BeautifulSoup
from django.db.models import TextField
from markdownify import markdownify as md
from wagtail_i18n.segments import SegmentValue, TemplateValue
from wagtail_i18n.segments.html import extract_html_segment, render_html_segment
from wagtail_i18n.segments.ingest import organise_template_segments

from core import validators as core_validators, widgets


class MarkdownField(TextField):
    def __init__(self, validators=None, *args, **kwargs):
        validators = validators or []
        if core_validators.slug_hyperlinks not in validators:
            validators.append(core_validators.slug_hyperlinks)
        super().__init__(validators=validators, *args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'widget': widgets.MarkdownTextarea
        }
        defaults.update(kwargs)
        return super(MarkdownField, self).formfield(**defaults)

    def get_translatable_segments(self, value):
        html = markdown.markdown(value)
        template, texts = extract_html_segment(html)

        return [
            TemplateValue('', 'html-formatted-markdown', template, len(texts))
        ] + [
            SegmentValue(str(position), text)
            for position, text in enumerate(texts)
        ]

    def restore_translated_segments(self, value, segments):
        format, template, texts = organise_template_segments(segments)
        assert format == 'html-formatted-markdown'
        html = render_html_segment(template, texts)
        return md(html)
