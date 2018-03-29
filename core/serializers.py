from rest_framework import fields
from wagtail.wagtailcore.rich_text import expand_db_html

from django.conf import settings
from django.utils import translation

from core import helpers


class URLHyperlinkSerializer(fields.CharField):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_attribute(self, instance):
        return instance.get_url(
            is_draft=helpers.is_draft_requested(self.context['request']),
            language_code=translation.get_language(),
        )


class APIRichTextSerializer(fields.CharField):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return expand_db_html(representation)


class APITranslationsSerializer(fields.ListField):
    def get_attribute(self, instance):
        return [
            (code, label) for (code, label) in settings.LANGUAGES_LOCALIZED
            if code in instance.translated_languages
        ]


class APIMetaSerializer(fields.DictField):

    languages = APITranslationsSerializer()
    url = URLHyperlinkSerializer()

    def get_attribute(self, instance):
        self.url.context = self.context
        return {
            'languages': self.languages.get_attribute(instance),
            'url': self.url.get_attribute(instance),
            'slug': instance.slug,
            'localised_urls': instance.get_localized_urls()
        }


class APIQuerysetSerializer(fields.ListField):
    def __init__(self, *args, **kwargs):
        self.fields_config = kwargs.pop('fields_config')
        self.queryset = kwargs.pop('queryset')
        super().__init__(*args, **kwargs)

    def get_attribute(self, instance):
        return instance

    def to_representation(self, instance):
        serializer_class = self.context['view']._get_serializer_class(
            router=self.context['router'],
            model=self.queryset.model,
            fields_config=self.fields_config,
        )
        serializer = serializer_class(
            self.queryset, many=True, context=self.context
        )
        return serializer.data
