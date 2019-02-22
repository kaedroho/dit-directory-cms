from rest_framework import serializers

from core import fields
from core.constants import COMPANY_SECTOR_CHOISES, EMPLOYEES_NUMBER_CHOISES, HEARD_ABOUT_CHOISES


class BasePageSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    seo_title = serializers.CharField()
    search_description = serializers.CharField()
    meta = fields.MetaDictField()
    full_url = serializers.CharField(max_length=255)
    full_path = serializers.CharField(
        max_length=255, source='specific.full_path')
    last_published_at = serializers.DateTimeField()
    title = serializers.CharField()
    page_type = serializers.SerializerMethodField()

    def get_page_type(self, instance):
        return instance.__class__.__name__


class FormPageSerializerMetaclass(serializers.SerializerMetaclass):
    """Metaclass that adds <field_name>_label and <field_name>_help_text to a
    serializer when given a list of form_field_names.
    """

    def __new__(mcls, name, bases, attrs):
        form_field_names = attrs['Meta'].model_class.form_field_names
        for field_name in form_field_names:
            attrs[field_name] = fields.FieldAttributesField()
        return super().__new__(mcls, name, bases, attrs)


class PagesTypesSerializer(serializers.Serializer):

    types = serializers.ListField(
        child=serializers.CharField()
    )


class WagtailPageSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    slug = serializers.CharField()


class DomesticContractForm(serializers.Serializer):
    contact_name = serializers.CharField()
    contact_email = serializers.EmailField(label='Contact Email')
    contact_number = serializers.IntegerField()
    company_name = serializers.CharField()
    company_location = serializers.CharField()
    sector = serializers.ChoiceField(choices=COMPANY_SECTOR_CHOISES)
    company_website = serializers.URLField()
    employees_number = serializers.ChoiceField(choices=EMPLOYEES_NUMBER_CHOISES)
    currently_export = serializers.BooleanField()
    advertising_feedback = serializers.ChoiceField(choices=HEARD_ABOUT_CHOISES)

