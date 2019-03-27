from uuid import UUID

from directory_constants.constants import cms
from django.core.exceptions import ValidationError
from django.forms import Textarea, CheckboxSelectMultiple
from django.utils.text import slugify
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.edit_handlers import (
    HelpPanel, FieldPanel, FieldRowPanel, MultiFieldPanel, PageChooserPanel
)
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail_i18n.models import Language, Locale, Region, TranslatablePageMixin

from django.db import models

from core.model_fields import MarkdownField

from core.models import (
    BasePage,
    ExclusivePageMixin,
    ServiceMixin,
)
from core.panels import SearchEngineOptimisationPanel
from export_readiness.models import Tag


class GreatInternationalApp(ExclusivePageMixin, ServiceMixin, BasePage):
    slug_identity = 'great-international-app'
    service_name_value = cms.GREAT_INTERNATIONAL

    @classmethod
    def allowed_subpage_models(cls):
        return [InternationalRegionRootPage,
                InternationalHomePage]


# Structural models

# Contains InternationalLocaleRootPage instances for a region
class InternationalRegionRootPage(BasePage):
    service_name_value = cms.GREAT_INTERNATIONAL

    region = models.OneToOneField(Region, on_delete=models.PROTECT, related_name='root_page')

    parent_page_types = ['GreatInternationalApp']
    subpage_types = ['InternationalLocaleRootPage']

    content_panels = [
        FieldPanel('region'),
    ]

    def clean(self):
        self.title = str(self.region.name)
        self.slug = self.region.slug

        return super().clean()


# Bucket of content for a locale (region/language combination) or core content
class InternationalLocaleRootPage(TranslatablePageMixin, BasePage):
    service_name_value = cms.GREAT_INTERNATIONAL

    # We use a constant value for "translation_key" as all locale root pages are translations of each other
    CONSTANT_TRANSLATION_KEY = UUID('e8114d17-1bca-48f2-b4cb-7c855eb0466b')

    language = models.ForeignKey(Language, on_delete=models.PROTECT, related_name='root_pages')

    parent_page_types = ['InternationalRegionRootPage']
    subpage_types = [
        'InternationalArticleListingPage',
        'InternationalTopicLandingPage',
        'InternationalCuratedTopicLandingPage',
        'InternationalLocalisedFolderPage'
    ]

    translatable_fields = []

    def save(self, *args, **kwargs):
        # Set translation_key and locale.
        # As this is the root page of the localised site, we must set this manually as
        # it doesn't have a translatable parent to inherit it from
        self.translation_key = self.CONSTANT_TRANSLATION_KEY

        self.title = self.language.get_display_name()

        if self.locale_id is None:
            language = self.language
            region = self.get_parent().specific.region
            self.locale = Locale.objects.filter(language=language, region=region).first()

        self.slug = self.language.code

        # Make sure a locale root page doesn't already exist for this locale
        # Note: Not bothering to filter on translation_key as all instances of this model should
        # have the same value for that
        other_root_pages = InternationalLocaleRootPage.objects.filter(locale=self.locale)

        if self.pk:
            other_root_pages = other_root_pages.exclude(pk=self.pk)
        if other_root_pages.exists():
            raise ValidationError({'language': ["A Locale Root Page with this language already exists in this region."]})

        return super().save(*args, **kwargs)

    content_panels = [
        FieldPanel('language'),
    ]


class InternationalSectorPage(TranslatablePageMixin, BasePage):
    service_name_value = cms.GREAT_INTERNATIONAL
    parent_page_types = ['great_international.InternationalTopicLandingPage']
    subpage_types = []

    tags = ParentalManyToManyField(Tag, blank=True)

    heading = models.CharField(max_length=255, verbose_name='Sector name')
    sub_heading = models.CharField(max_length=255, blank=True)
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    heading_teaser = models.TextField(blank=True, verbose_name='Introduction')

    section_one_body = MarkdownField(
        null=True,
        verbose_name='3 unique selling points markdown'
    )
    section_one_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Image for unique selling points'
    )
    section_one_image_caption = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Image caption')
    section_one_image_caption_company = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Image caption attribution')

    statistic_1_number = models.CharField(max_length=255)
    statistic_1_heading = models.CharField(max_length=255)
    statistic_1_smallprint = models.CharField(max_length=255, blank=True)

    statistic_2_number = models.CharField(max_length=255)
    statistic_2_heading = models.CharField(max_length=255)
    statistic_2_smallprint = models.CharField(max_length=255, blank=True)

    statistic_3_number = models.CharField(max_length=255, blank=True)
    statistic_3_heading = models.CharField(max_length=255, blank=True)
    statistic_3_smallprint = models.CharField(max_length=255, blank=True)

    statistic_4_number = models.CharField(max_length=255, blank=True)
    statistic_4_heading = models.CharField(max_length=255, blank=True)
    statistic_4_smallprint = models.CharField(max_length=255, blank=True)

    statistic_5_number = models.CharField(max_length=255, blank=True)
    statistic_5_heading = models.CharField(max_length=255, blank=True)
    statistic_5_smallprint = models.CharField(max_length=255, blank=True)

    statistic_6_number = models.CharField(max_length=255, blank=True)
    statistic_6_heading = models.CharField(max_length=255, blank=True)
    statistic_6_smallprint = models.CharField(max_length=255, blank=True)

    section_two_heading = models.CharField(
        max_length=255,
        verbose_name='Spotlight'
    )
    section_two_teaser = models.TextField(
        verbose_name='Spotlight summary'
    )

    section_two_subsection_one_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Spotlight 1 icon'
    )
    section_two_subsection_one_heading = models.CharField(
        max_length=255,
        verbose_name='Spotlight 1 heading'
    )
    section_two_subsection_one_body = models.TextField(
        verbose_name='Spotlight 1 body'
    )

    section_two_subsection_two_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Spotlight 2 icon'
    )
    section_two_subsection_two_heading = models.CharField(
        max_length=255,
        verbose_name='Spotlight 2 heading'
    )
    section_two_subsection_two_body = models.TextField(
        verbose_name='Spotlight 2 body'
    )

    section_two_subsection_three_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Spotlight 3 icon'
    )
    section_two_subsection_three_heading = models.CharField(
        max_length=255,
        verbose_name='Spotlight 3 heading'
    )
    section_two_subsection_three_body = models.TextField(
        verbose_name='Spotlight 3 body'
    )

    case_study_title = models.CharField(max_length=255, blank=True)
    case_study_description = models.CharField(max_length=255, blank=True)
    case_study_cta_text = models.TextField(
        blank=True,
        verbose_name='Case study link text'
    )
    case_study_cta_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Case study link URL'
    )
    case_study_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    section_three_heading = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Fact sheets heading'
    )
    section_three_teaser = models.TextField(
        blank=True,
        verbose_name='Fact sheets teaser'
    )

    section_three_subsection_one_heading = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Fact sheet 1 heading'
    )
    section_three_subsection_one_teaser = models.TextField(
        blank=True,
        verbose_name='Fact sheet 1 teaser'
    )
    section_three_subsection_one_body = MarkdownField(
        blank=True,
        null=True,
        verbose_name='Fact sheet 1 body'
    )

    section_three_subsection_two_heading = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Fact sheet 2 heading'
    )
    section_three_subsection_two_teaser = models.TextField(
        blank=True,
        verbose_name='Fact sheet 2 teaser'
    )
    section_three_subsection_two_body = MarkdownField(
        blank=True,
        null=True,
        verbose_name='Fact sheet 2 body'
    )

    related_page_one = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    related_page_two = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    related_page_three = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    translatable_fields = [
        'title',
        'slug',
        # 'tags'
        'heading',
        'sub_heading',
        'hero_image',
        'heading_teaser',
        'section_one_body',
        #'section_one_image',
        'section_one_image_caption',
        'section_one_image_caption_company',
        'statistic_1_heading',
        'statistic_1_smallprint',
        'statistic_2_heading',
        'statistic_2_smallprint',
        'statistic_3_heading',
        'statistic_3_smallprint',
        'statistic_4_heading',
        'statistic_4_smallprint',
        'statistic_5_heading',
        'statistic_5_smallprint',
        'statistic_6_heading',
        'statistic_6_smallprint',
        'section_two_heading',
        'section_two_teaser',
        #'section_two_subsection_one_icon',
        'section_two_subsection_one_heading',
        'section_two_subsection_one_body',
        #'section_two_subsection_two_icon',
        'section_two_subsection_two_heading',
        'section_two_subsection_two_body',
        #'section_two_subsection_three_icon',
        'section_two_subsection_three_heading',
        'section_two_subsection_three_body',
        'case_study_title',
        'case_study_description',
        'case_study_cta_text',
        #'case_study_image',
        'section_three_heading',
        'section_three_teaser',
        'section_three_subsection_one_heading',
        'section_three_subsection_one_teaser',
        'section_three_subsection_one_body',
        'section_three_subsection_two_heading',
        'section_three_subsection_two_teaser',
        'section_three_subsection_two_body',
    ]

    content_panels = [
        MultiFieldPanel(
            heading='Heading',
            children=[
                FieldPanel('heading'),
                FieldPanel('sub_heading'),
                ImageChooserPanel('hero_image'),
                FieldPanel('heading_teaser')
            ]

        ),
        MultiFieldPanel(
            heading='Unique selling points',
            children=[
                HelpPanel(
                    'Use H2 (##) markdown for the three subheadings'),
                FieldRowPanel(
                    [
                        FieldPanel('section_one_body'),
                        MultiFieldPanel(
                            [
                                ImageChooserPanel('section_one_image'),
                                FieldPanel('section_one_image_caption'),
                                FieldPanel('section_one_image_caption_company')
                            ]
                        )
                    ]
                )
            ]
        ),
        MultiFieldPanel(
            heading='Statistics',
            children=[
                FieldRowPanel(
                    [
                        MultiFieldPanel(
                            [
                                FieldPanel('statistic_1_number'),
                                FieldPanel('statistic_1_heading'),
                                FieldPanel('statistic_1_smallprint')
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('statistic_2_number'),
                                FieldPanel('statistic_2_heading'),
                                FieldPanel('statistic_2_smallprint')
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('statistic_3_number'),
                                FieldPanel('statistic_3_heading'),
                                FieldPanel('statistic_3_smallprint')
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('statistic_4_number'),
                                FieldPanel('statistic_4_heading'),
                                FieldPanel('statistic_4_smallprint')
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('statistic_5_number'),
                                FieldPanel('statistic_5_heading'),
                                FieldPanel('statistic_5_smallprint')
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel('statistic_6_number'),
                                FieldPanel('statistic_6_heading'),
                                FieldPanel('statistic_6_smallprint')
                            ]
                        ),
                    ]
                )
            ]
        ),
        MultiFieldPanel(
            heading='Spotlight',
            children=[
                FieldPanel('section_two_heading'),
                FieldPanel('section_two_teaser'),
                FieldRowPanel(
                    [
                        MultiFieldPanel(
                            [
                                ImageChooserPanel(
                                    'section_two_subsection_one_icon'),
                                FieldPanel(
                                    'section_two_subsection_one_heading'),
                                FieldPanel(
                                    'section_two_subsection_one_body')
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                ImageChooserPanel(
                                    'section_two_subsection_two_icon'),
                                FieldPanel(
                                    'section_two_subsection_two_heading'),
                                FieldPanel(
                                    'section_two_subsection_two_body')
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                ImageChooserPanel(
                                    'section_two_subsection_three_icon'),
                                FieldPanel(
                                    'section_two_subsection_three_heading'),
                                FieldPanel(
                                    'section_two_subsection_three_body')
                            ]
                        )
                    ]
                )
            ]
        ),
        MultiFieldPanel(
            heading='Case Study',
            classname='collapsible',
            children=[
                FieldPanel('case_study_title'),
                FieldPanel('case_study_description'),
                FieldPanel('case_study_cta_text'),
                PageChooserPanel(
                    'case_study_cta_page',
                    [
                        'great_international.InternationalArticlePage',
                        'great_international.InternationalCampaignPage',
                    ]),
                ImageChooserPanel('case_study_image')
            ]
        ),
        MultiFieldPanel(
            heading='Fact Sheets',
            classname='collapsible collapsed',
            children=[
                FieldPanel('section_three_heading'),
                FieldPanel('section_three_teaser'),
                FieldRowPanel(
                    [
                        MultiFieldPanel(
                            [
                                FieldPanel(
                                    'section_three_subsection_one_heading'),
                                FieldPanel(
                                    'section_three_subsection_one_teaser'),
                                HelpPanel(
                                    'For accessibility reasons, use only '
                                    '"#### [Your text here]" for subheadings '
                                    'in this markdown field'),
                                FieldPanel(
                                    'section_three_subsection_one_body')
                            ]
                        ),
                        MultiFieldPanel(
                            [
                                FieldPanel(
                                    'section_three_subsection_two_heading'),
                                FieldPanel(
                                    'section_three_subsection_two_teaser'),
                                HelpPanel(
                                    'For accessibility reasons, use only '
                                    '"#### [Your text here]" for subheadings '
                                    'in this markdown field'),
                                FieldPanel(
                                    'section_three_subsection_two_body')
                            ]
                        )
                    ]
                )
            ]
        ),
        MultiFieldPanel(
            heading='Related articles',
            children=[
                FieldRowPanel([
                    PageChooserPanel(
                        'related_page_one',
                        [
                            'great_international.InternationalArticlePage',
                            'great_international.InternationalCampaignPage',
                        ]),
                    PageChooserPanel(
                        'related_page_two',
                        [
                            'great_international.InternationalArticlePage',
                            'great_international.InternationalCampaignPage',
                        ]),
                    PageChooserPanel(
                        'related_page_three',
                        [
                            'great_international.InternationalArticlePage',
                            'great_international.InternationalCampaignPage',
                        ]),
                ])
            ]
        ),
        SearchEngineOptimisationPanel()
    ]

    settings_panels = [
        FieldPanel('title'),
        FieldPanel('slug'),
        FieldPanel('tags', widget=CheckboxSelectMultiple)
    ]


class InternationalHomePage(ExclusivePageMixin, BasePage):
    service_name_value = cms.GREAT_INTERNATIONAL
    slug_identity = cms.GREAT_HOME_INTERNATIONAL_SLUG
    subpage_types = []

    tariffs_title = models.CharField(max_length=255)
    tariffs_description = MarkdownField()
    tariffs_link = models.URLField()
    tariffs_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    news_title = models.CharField(max_length=255)
    related_page_one = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    related_page_two = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    related_page_three = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    content_panels = [
        MultiFieldPanel(
            heading='Tariffs',
            children=[
                FieldPanel('tariffs_title'),
                FieldPanel('tariffs_description'),
                FieldPanel('tariffs_link'),
                ImageChooserPanel('tariffs_image')
            ]
        ),
        MultiFieldPanel(
            heading='News section',
            children=[
                FieldPanel('news_title'),
                FieldRowPanel([
                    PageChooserPanel(
                        'related_page_one',
                        [
                            'great_international.InternationalArticlePage',
                            'great_international.InternationalCampaignPage',
                        ]),
                    PageChooserPanel(
                        'related_page_two',
                        [
                            'great_international.InternationalArticlePage',
                            'great_international.InternationalCampaignPage',
                        ]),
                    PageChooserPanel(
                        'related_page_three',
                        [
                            'great_international.InternationalArticlePage',
                            'great_international.InternationalCampaignPage',
                        ]),
                ])
            ]
        ),
        SearchEngineOptimisationPanel(),
    ]

    settings_panels = [
        FieldPanel('title'),
        FieldPanel('slug'),
    ]


# DELETEME: No longer required
class InternationalRegionPage(BasePage):
    creatable = False

    service_name_value = cms.GREAT_INTERNATIONAL
    parent_page_types = ['great_international.GreatInternationalApp']
    subpage_types = [
        'great_international.InternationalLocalisedFolderPage'
    ]

    tags = ParentalManyToManyField(Tag, blank=True)

    settings_panels = [
        FieldPanel('title'),
        FieldPanel('slug'),
        FieldPanel('tags', widget=CheckboxSelectMultiple)
    ]

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


# DELETEME: No longer required
class InternationalLocalisedFolderPage(BasePage):
    service_name_value = cms.GREAT_INTERNATIONAL
    parent_page_types = ['great_international.InternationalRegionPage']
    subpage_types = [
        'great_international.InternationalArticlePage',
        'great_international.InternationalCampaignPage'
    ]

    settings_panels = [
        FieldPanel('title'),
        FieldPanel('slug'),
    ]

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = slugify(f'{self.slug}-{self.get_parent().slug}')
        return super().save(*args, **kwargs)


class InternationalArticlePage(TranslatablePageMixin, BasePage):
    service_name_value = cms.GREAT_INTERNATIONAL
    parent_page_types = [
        'great_international.InternationalArticleListingPage',
        'great_international.InternationalCampaignPage',
        'great_international.InternationalLocalisedFolderPage',
        'great_international.InternationalCuratedTopicLandingPage',
        'great_international.InternationalGuideLandingPage',
    ]
    subpage_types = []

    article_title = models.CharField(max_length=255)

    article_teaser = models.CharField(max_length=255)
    article_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    article_body_text = MarkdownField()

    related_page_one = models.ForeignKey(
        'great_international.InternationalArticlePage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    related_page_two = models.ForeignKey(
        'great_international.InternationalArticlePage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    related_page_three = models.ForeignKey(
        'great_international.InternationalArticlePage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    tags = ParentalManyToManyField(Tag, blank=True)

    translatable_fields = [
        'title',
        'slug',
        'article_title',
        'article_teaser',
        #'article_image',
        'article_body_text',
        #'tags',
    ]

    content_panels = [
        FieldPanel('article_title'),
        MultiFieldPanel(
            heading='Article content',
            children=[
                FieldPanel('article_teaser'),
                ImageChooserPanel('article_image'),
                FieldPanel('article_body_text')
            ]
        ),
        MultiFieldPanel(
            heading='Related articles',
            children=[
                FieldRowPanel([
                    PageChooserPanel(
                        'related_page_one',
                        'great_international.InternationalArticlePage'),
                    PageChooserPanel(
                        'related_page_two',
                        'great_international.InternationalArticlePage'),
                    PageChooserPanel(
                        'related_page_three',
                        'great_international.InternationalArticlePage'),
                ]),
            ]
        ),
        SearchEngineOptimisationPanel(),
    ]

    settings_panels = [
        FieldPanel('title'),
        FieldPanel('slug'),
        FieldPanel('tags', widget=CheckboxSelectMultiple)
    ]


class InternationalArticleListingPage(TranslatablePageMixin, BasePage):
    service_name_value = cms.GREAT_INTERNATIONAL
    parent_page_types = [
        'great_international.InternationalLocaleRootPage',
        'great_international.InternationalTopicLandingPage'
    ]
    subpage_types = [
        'great_international.InternationalArticlePage',
        'great_international.InternationalCampaignPage',
    ]

    landing_page_title = models.CharField(max_length=255)
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    hero_teaser = models.CharField(max_length=255, null=True, blank=True)
    list_teaser = MarkdownField(null=True, blank=True)
    tags = ParentalManyToManyField(Tag, blank=True)

    translatable_fields = [
        'title',
        'slug',
        'landing_page_title',
        #'hero_image',
        'hero_teaser',
        'list_teaser',
        #'tags',
    ]

    @property
    def articles_count(self):
        return self.get_descendants().type(
            InternationalArticlePage
        ).live().count()

    content_panels = [
        FieldPanel('landing_page_title'),
        MultiFieldPanel(
            heading='Hero',
            children=[
                ImageChooserPanel('hero_image'),
                FieldPanel('hero_teaser')
            ]
        ),
        FieldPanel('list_teaser'),
        SearchEngineOptimisationPanel(),
    ]

    settings_panels = [
        FieldPanel('title'),
        FieldPanel('slug'),
        FieldPanel('tags', widget=CheckboxSelectMultiple)
    ]


class InternationalCampaignPage(TranslatablePageMixin, BasePage):
    service_name_value = cms.GREAT_INTERNATIONAL
    parent_page_types = [
        'great_international.InternationalArticleListingPage',
        'great_international.InternationalTopicLandingPage',
        'great_international.InternationalLocalisedFolderPage'
    ]
    subpage_types = [
        'great_international.InternationalArticlePage'
    ]
    view_path = 'campaigns/'

    campaign_teaser = models.CharField(max_length=255, null=True, blank=True)
    campaign_heading = models.CharField(max_length=255)
    campaign_hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    section_one_heading = models.CharField(max_length=255)
    section_one_intro = MarkdownField()
    section_one_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    selling_point_one_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    selling_point_one_heading = models.CharField(max_length=255)
    selling_point_one_content = MarkdownField()

    selling_point_two_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    selling_point_two_heading = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    selling_point_two_content = MarkdownField(null=True, blank=True)

    selling_point_three_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    selling_point_three_heading = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    selling_point_three_content = MarkdownField(null=True, blank=True)

    section_one_contact_button_url = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    section_one_contact_button_text = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    section_two_heading = models.CharField(max_length=255)
    section_two_intro = MarkdownField()

    section_two_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    section_two_contact_button_url = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    section_two_contact_button_text = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    related_content_heading = models.CharField(max_length=255)
    related_content_intro = MarkdownField()

    related_page_one = models.ForeignKey(
        'great_international.InternationalArticlePage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    related_page_two = models.ForeignKey(
        'great_international.InternationalArticlePage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    related_page_three = models.ForeignKey(
        'great_international.InternationalArticlePage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    cta_box_message = models.CharField(max_length=255)
    cta_box_button_url = models.CharField(max_length=255)
    cta_box_button_text = models.CharField(max_length=255)

    tags = ParentalManyToManyField(Tag, blank=True)

    translatable_fields = [
        'title',
        'slug',
        'campaign_teaser',
        'campaign_heading',
        #'campaign_hero_image',
        'section_one_heading',
        'section_one_intro',
        #'section_one_image',
        #'selling_point_one_icon',
        'selling_point_one_heading',
        'selling_point_one_content',
        #'selling_point_two_icon',
        'selling_point_two_heading',
        'selling_point_two_content',
        #'selling_point_three_icon',
        'selling_point_three_heading',
        'selling_point_three_content',
        'section_one_contact_button_text',
        'section_two_heading',
        'section_two_intro',
        #'section_two_image',
        'section_two_contact_button_text',
        'related_content_heading',
        'related_content_intro',
        'cta_box_message',
        'cta_box_button_text',
        #'tags',
    ]

    content_panels = [
        MultiFieldPanel(
            heading='Hero section',
            children=[
                FieldPanel('campaign_heading'),
                FieldPanel('campaign_teaser'),
                ImageChooserPanel('campaign_hero_image'),
            ]
        ),
        MultiFieldPanel(
            heading='Section one',
            children=[
                FieldPanel('section_one_heading'),
                FieldPanel('section_one_intro'),
                ImageChooserPanel('section_one_image'),
                FieldRowPanel([
                    MultiFieldPanel(
                        children=[
                            ImageChooserPanel('selling_point_one_icon'),
                            FieldPanel('selling_point_one_heading'),
                            FieldPanel('selling_point_one_content'),
                        ]
                    ),
                    MultiFieldPanel(
                        children=[
                            ImageChooserPanel('selling_point_two_icon'),
                            FieldPanel('selling_point_two_heading'),
                            FieldPanel('selling_point_two_content'),
                        ]
                    ),
                    MultiFieldPanel(
                        children=[
                            ImageChooserPanel('selling_point_three_icon'),
                            FieldPanel('selling_point_three_heading'),
                            FieldPanel('selling_point_three_content'),
                        ]
                    ),
                ]),
                FieldRowPanel([
                    FieldPanel('section_one_contact_button_text'),
                    FieldPanel('section_one_contact_button_url'),
                ])
            ]
        ),
        MultiFieldPanel(
            heading='Section two',
            children=[
                FieldPanel('section_two_heading'),
                FieldPanel('section_two_intro'),
                ImageChooserPanel('section_two_image'),
                FieldRowPanel([
                    FieldPanel('section_two_contact_button_text'),
                    FieldPanel('section_two_contact_button_url'),
                ])
            ]
        ),
        MultiFieldPanel(
            heading='Related content section',
            children=[
                FieldPanel('related_content_heading'),
                FieldPanel('related_content_intro'),
                FieldRowPanel([
                    PageChooserPanel(
                        'related_page_one',
                        'great_international.InternationalArticlePage'),
                    PageChooserPanel(
                        'related_page_two',
                        'great_international.InternationalArticlePage'),
                    PageChooserPanel(
                        'related_page_three',
                        'great_international.InternationalArticlePage'),
                ])
            ]
        ),
        MultiFieldPanel(
            heading='Contact box',
            children=[
                FieldRowPanel([
                    FieldPanel('cta_box_message', widget=Textarea),
                    MultiFieldPanel([
                        FieldPanel('cta_box_button_url'),
                        FieldPanel('cta_box_button_text'),
                    ])
                ])
            ]
        ),
        SearchEngineOptimisationPanel(),
    ]

    settings_panels = [
        FieldPanel('title'),
        FieldPanel('slug'),
        FieldPanel('tags', widget=CheckboxSelectMultiple)
    ]


class InternationalTopicLandingPage(TranslatablePageMixin, BasePage):
    service_name_value = cms.GREAT_INTERNATIONAL
    parent_page_types = ['great_international.InternationalLocaleRootPage']
    subpage_types = [
        'great_international.InternationalArticleListingPage',
        'great_international.InternationalCampaignPage',
        'great_international.InternationalGuideLandingPage',
        'great_international.InternationalSectorPage',
    ]

    landing_page_title = models.CharField(max_length=255)

    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    hero_teaser = models.CharField(max_length=255, null=True, blank=True)
    tags = ParentalManyToManyField(Tag, blank=True)

    translatable_fields = [
        'title',
        'slug',
        'landing_page_title',
        #'hero_image',
        'hero_teaser',
        #'tags',
    ]

    content_panels = [
        FieldPanel('landing_page_title'),
        MultiFieldPanel(
            heading='Hero',
            children=[
                ImageChooserPanel('hero_image'),
                FieldPanel('hero_teaser')
            ]
        ),
        SearchEngineOptimisationPanel(),
    ]

    settings_panels = [
        FieldPanel('title'),
        FieldPanel('slug'),
        FieldPanel('tags', widget=CheckboxSelectMultiple)
    ]


class InternationalCuratedTopicLandingPage(TranslatablePageMixin, BasePage):
    service_name_value = cms.GREAT_INTERNATIONAL
    parent_page_types = ['great_international.InternationalLocaleRootPage']
    subpage_types = [
        'great_international.InternationalArticlePage',
        'great_international.InternationalGuideLandingPage',
    ]

    display_title = models.CharField(max_length=255, blank=True, null=True)

    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    teaser = models.CharField(max_length=255)

    feature_section_heading = models.CharField(max_length=255)

    feature_one_heading = models.CharField(max_length=100)
    feature_one_image = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name="image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    feature_one_content = MarkdownField(verbose_name="content")

    feature_two_heading = models.CharField(max_length=100)
    feature_two_image = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name="image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    feature_two_content = MarkdownField(verbose_name="content")

    feature_three_heading = models.CharField(max_length=100)
    feature_three_image = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name="image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    feature_three_url = models.URLField(verbose_name="URL")

    feature_four_heading = models.CharField(max_length=100)
    feature_four_image = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name="image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    feature_four_url = models.URLField(verbose_name="URL")

    feature_five_heading = models.CharField(max_length=100)
    feature_five_image = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name="image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    feature_five_url = models.URLField(verbose_name="URL")

    tags = ParentalManyToManyField(Tag, blank=True)

    translatable_fields = [
        'title',
        'slug',
        'display_title',
        #'hero_image',
        'teaser',
        'feature_section_heading',
        'feature_one_heading',
        #'feature_one_image',
        'feature_one_content',
        'feature_two_heading',
        #'feature_two_image',
        'feature_two_content',
        'feature_three_heading',
        #'feature_three_image',
        'feature_four_heading',
        #'feature_four_image',
        'feature_five_heading',
        #'feature_five_image',
        #'tags',
    ]

    content_panels = [
        FieldPanel('display_title'),
        ImageChooserPanel('hero_image'),
        FieldPanel('teaser'),
        MultiFieldPanel(
            heading="featured content section",
            children=[
                FieldPanel('feature_section_heading'),
                FieldRowPanel([
                    MultiFieldPanel([
                        FieldPanel('feature_one_heading'),
                        ImageChooserPanel('feature_one_image'),
                        FieldPanel('feature_one_content'),
                    ]),
                    MultiFieldPanel([
                        FieldPanel('feature_two_heading'),
                        ImageChooserPanel('feature_two_image'),
                        FieldPanel('feature_two_content'),
                    ]),
                ]),
                FieldRowPanel([
                    MultiFieldPanel([
                        FieldPanel('feature_three_heading'),
                        ImageChooserPanel('feature_three_image'),
                        FieldPanel('feature_three_url'),
                    ]),
                    MultiFieldPanel([
                        FieldPanel('feature_four_heading'),
                        ImageChooserPanel('feature_four_image'),
                        FieldPanel('feature_four_url'),
                    ]),
                    MultiFieldPanel([
                        FieldPanel('feature_five_heading'),
                        ImageChooserPanel('feature_five_image'),
                        FieldPanel('feature_five_url'),
                    ]),
                ]),
            ]
        )
    ]

    settings_panels = [
        FieldPanel('title'),
        SearchEngineOptimisationPanel(),
        FieldPanel('slug'),
        FieldPanel('tags', widget=CheckboxSelectMultiple)
    ]


class InternationalGuideLandingPage(TranslatablePageMixin, BasePage):
    service_name_value = cms.GREAT_INTERNATIONAL
    parent_page_types = [
        'great_international.InternationalCuratedTopicLandingPage',
        'great_international.InternationalTopicLandingPage',
    ]
    subpage_types = [
        'great_international.InternationalArticlePage',
    ]

    display_title = models.CharField(max_length=255)

    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    teaser = models.CharField(max_length=255)

    section_one_content = MarkdownField(verbose_name="content")
    section_one_image = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name="image",
        null=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    section_one_image_caption = models.CharField(
        verbose_name="image caption",
        max_length=100,
        blank=True,
        null=True,
    )

    section_two_heading = models.CharField(
        verbose_name="heading",
        max_length=100
    )
    section_two_teaser = models.TextField(verbose_name="teaser")
    section_two_button_text = models.CharField(
        verbose_name="button text",
        max_length=100
    )
    section_two_button_url = models.CharField(
        verbose_name="button URL",
        max_length=255
    )
    section_two_image = models.ForeignKey(
        'wagtailimages.Image',
        verbose_name="image",
        null=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    guides_section_heading = models.CharField(
        verbose_name="section heading",
        max_length=100,
    )

    tags = ParentalManyToManyField(Tag, blank=True)

    translatable_fields = [
        'title',
        'slug',
        'display_title',
        #'hero_image',
        'teaser',
        'section_one_content',
        #'section_one_image',
        'section_one_image_caption',
        'section_two_heading',
        'section_two_teaser',
        'section_two_button_text',
        #'section_two_image',
        'guides_section_heading',
        #'tags',
    ]

    content_panels = [
        FieldPanel('display_title'),
        ImageChooserPanel('hero_image'),
        FieldPanel('teaser'),
        MultiFieldPanel(
            heading="Attractive features",
            children=[
                FieldPanel('section_one_content'),
                HelpPanel(
                    'For accessibility reasons, use only '
                    '"#### [Your text here]" for subheadings '
                    'in this markdown field'
                ),
                ImageChooserPanel('section_one_image'),
                FieldPanel('section_one_image_caption'),
            ]
        ),
        MultiFieldPanel(
            heading="Feature banner",
            children=[
                FieldPanel('section_two_heading'),
                FieldPanel('section_two_teaser'),
                FieldPanel('section_two_button_text'),
                FieldPanel('section_two_button_url'),
                ImageChooserPanel('section_two_image'),
            ]
        ),
        MultiFieldPanel(
            heading="Guides section",
            children=[
                FieldPanel('guides_section_heading'),
            ]
        )
    ]

    settings_panels = [
        FieldPanel('title'),
        SearchEngineOptimisationPanel(),
        FieldPanel('slug'),
        FieldPanel('tags', widget=CheckboxSelectMultiple)
    ]
