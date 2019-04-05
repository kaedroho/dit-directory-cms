from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from django.utils import translation
from modelcluster.models import get_all_child_relations
from modeltranslation.translator import translator
from modeltranslation.utils import build_localized_fieldname

from wagtail.core.models import Page
from wagtail_i18n.models import Language, Locale, TranslatablePageMixin

from invest.models import InvestApp, InvestLocaleRootPage


class Command(BaseCommand):
    @transaction.atomic
    def restructure_existing_pages(self):
        if InvestLocaleRootPage.objects.exists():
            print("A locale root page already exists")
            return

        invest_app_root = InvestApp.objects.get()

        print("Creating locale root")
        default_locale = Locale.objects.default()
        locale_root = invest_app_root.add_child(instance=InvestLocaleRootPage(
            locale=Locale.objects.default(),
        ))

        for page in invest_app_root.get_children().exclude(id=locale_root.id).specific():
            if not isinstance(page, TranslatablePageMixin):
                # Keep non-translatable pages at the root
                continue

            print("Moving", page.title)
            page.move(locale_root, pos='last-child')

    def handle(self, **options):
        self.restructure_existing_pages()

        page_models = [
            model for model in translator.get_registered_models()
            if model._meta.app_label == 'invest' and issubclass(model, TranslatablePageMixin)
        ]

        for language in dict(settings.LANGUAGES).keys():
            locale = Locale.objects.get(region__is_default=True, language__code=language)
            if locale.language == Language.default():
                continue

            try:
                with translation.override(language):
                    for page in Page.objects.type(tuple(page_models)).order_by('path').specific():
                        model = page.specific_class

                        if page.has_translation(locale):
                            continue

                        page.title = page.title or getattr(page, 'title_en_gb', None)

                        # Exclude all "translated" child relation fields
                        # This is to prevent multiple copies of the same child objects being made which causes unique key errors
                        exclude_fields = []
                        opts = translator.get_options_for_model(model)
                        for field_name in opts.related_fields:
                            exclude_fields.extend(
                            build_localized_fieldname(field_name, lang) for lang in dict(settings.LANGUAGES).keys()
                        )

                        try:
                            result = page.copy_for_translation(locale, copy_parents=True, exclude_fields=exclude_fields)

                            if result:
                                if page.live:
                                    result.get_latest_revision().publish()

                                print("SUCCESS")
                            else:
                                print("FAIL")
                        except ValidationError as e:
                            print("VALIDATION ERROR")
                            print(e)
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                import pdb, traceback, sys
                extype, value, tb = sys.exc_info()
                traceback.print_exc()
                pdb.post_mortem(tb)
