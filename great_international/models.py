from wagtail.documents.models import Document
from wagtail.documents.edit_handlers import DocumentChooserPanel

from directory_constants.constants import cms
from django.forms import Textarea, CheckboxSelectMultiple
from django.utils.text import slugify
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.edit_handlers import (
    HelpPanel, FieldPanel, FieldRowPanel, MultiFieldPanel, PageChooserPanel
)
from wagtail.images.edit_handlers import ImageChooserPanel

from core.helpers import make_translated_interface
from django.db import models

from core.helpers import make_translated_interface
from core.model_fields import MarkdownField

from core.models import (
    BasePage,
    ExclusivePageMixin,
    ServiceMixin,
)
from core.mixins import ServiceHomepageMixin
from core.panels import SearchEngineOptimisationPanel
from export_readiness.models import Tag


class GreatInternationalApp(ExclusivePageMixin, ServiceMixin, BasePage):
    slug_identity = 'great-international-app'
    service_name_value = cms.GREAT_INTERNATIONAL

    @classmethod
    def get_required_translatable_fields(cls):
        return []

    @classmethod
    def allowed_subpage_models(cls):
        return [InternationalArticleListingPage,
                InternationalTopicLandingPage,
                InternationalCuratedTopicLandingPage,
                InternationalRegionPage,
                InternationalHomePage,
                InternationalCapitalInvestLandingPage]


class InternationalSectorPage(BasePage):

    class Meta:
        ordering = ['-heading']

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
    case_study_description = models.TextField(blank=True)
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
        FieldPanel('title_en_gb'),
        FieldPanel('slug'),
        FieldPanel('tags', widget=CheckboxSelectMultiple)
    ]

    edit_handler = make_translated_interface(
        content_panels=content_panels,
        settings_panels=settings_panels
    )


class InternationalHomePage(
    ExclusivePageMixin, ServiceHomepageMixin, BasePage
):
    service_name_value = cms.GREAT_INTERNATIONAL
    slug_identity = cms.GREAT_HOME_INTERNATIONAL_SLUG
    subpage_types = []

    hero_title = models.CharField(max_length=255)
    hero_subtitle = models.CharField(max_length=255, blank=True)
    hero_cta_text = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    hero_cta_link = models.CharField(max_length=255, blank=True)
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    invest_title = models.CharField(max_length=255)
    invest_content = MarkdownField(blank=True)
    invest_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    trade_title = models.CharField(max_length=255)
    trade_content = MarkdownField(blank=True)
    trade_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

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
    tariffs_call_to_action_text = models.CharField(max_length=255)

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

    study_in_uk_cta_text = models.CharField(max_length=255)
    visit_uk_cta_text = models.CharField(max_length=255)

    content_panels = [
        MultiFieldPanel(
            heading="Hero Section",
            children=[
                FieldPanel('hero_title'),
                FieldPanel('hero_subtitle'),
                FieldPanel("hero_cta_text"),
                FieldPanel("hero_cta_link"),
                ImageChooserPanel("hero_image")
            ]
        ),
        MultiFieldPanel(
            heading="Featured Cards",
            children=[
                FieldRowPanel([
                    MultiFieldPanel(
                        heading='Invest Card',
                        children=[
                            FieldPanel('invest_title'),
                            FieldPanel('invest_content'),
                            ImageChooserPanel('invest_image')
                        ]
                    ),
                    MultiFieldPanel(
                        heading='Trade Card',
                        children=[
                            FieldPanel('trade_title'),
                            FieldPanel('trade_content'),
                            ImageChooserPanel('trade_image')
                        ]
                    ),
                ]),
            ]
        ),

        MultiFieldPanel(
            heading='Tariffs',
            children=[
                FieldPanel('tariffs_title'),
                FieldPanel('tariffs_description'),
                FieldPanel('tariffs_link'),
                ImageChooserPanel('tariffs_image'),
                FieldPanel('tariffs_call_to_action_text')
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

        MultiFieldPanel(
            heading='Featured CTA\'s',
            children=[
                FieldRowPanel([
                    MultiFieldPanel(
                        heading="Study in the UK",
                        children=[
                            FieldPanel('study_in_uk_cta_text')
                        ]
                    ),
                    MultiFieldPanel(
                        heading="Visit the UK",
                        children=[
                            FieldPanel('visit_uk_cta_text')
                        ]
                    ),
                ]),
            ]
        ),

        SearchEngineOptimisationPanel(),
    ]

    settings_panels = [
        FieldPanel('title_en_gb'),
        FieldPanel('slug'),
    ]

    edit_handler = make_translated_interface(
        content_panels=content_panels,
        settings_panels=settings_panels
    )


class InternationalRegionPage(BasePage):
    service_name_value = cms.GREAT_INTERNATIONAL
    parent_page_types = ['great_international.GreatInternationalApp']
    subpage_types = [
        'great_international.InternationalLocalisedFolderPage'
    ]

    tags = ParentalManyToManyField(Tag, blank=True)

    settings_panels = [
        FieldPanel('title_en_gb'),
        FieldPanel('slug'),
        FieldPanel('tags', widget=CheckboxSelectMultiple)
    ]

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class InternationalLocalisedFolderPage(BasePage):
    service_name_value = cms.GREAT_INTERNATIONAL
    parent_page_types = ['great_international.InternationalRegionPage']
    subpage_types = [
        'great_international.InternationalArticlePage',
        'great_international.InternationalCampaignPage'
    ]

    settings_panels = [
        FieldPanel('title_en_gb'),
        FieldPanel('slug'),
    ]

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = slugify(f'{self.slug}-{self.get_parent().slug}')
        return super().save(*args, **kwargs)


class InternationalArticlePage(BasePage):
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
    article_subheading = models.CharField(
        max_length=255,
        blank=True,
        help_text="This is a subheading that displays "
                  "below the main title on the article page"
    )
    article_teaser = models.CharField(
        max_length=255,
        help_text="This is a subheading that displays when the article "
                  "is featured on another page"
    )
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

    content_panels = [
        FieldPanel('article_title'),
        MultiFieldPanel(
            heading='Article content',
            children=[
                FieldPanel('article_subheading'),
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
        FieldPanel('title_en_gb'),
        FieldPanel('slug'),
        FieldPanel('tags', widget=CheckboxSelectMultiple)
    ]

    edit_handler = make_translated_interface(
        content_panels=content_panels,
        settings_panels=settings_panels
    )


class InternationalArticleListingPage(BasePage):
    service_name_value = cms.GREAT_INTERNATIONAL
    parent_page_types = [
        'great_international.GreatInternationalApp',
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
        FieldPanel('title_en_gb'),
        FieldPanel('slug'),
        FieldPanel('tags', widget=CheckboxSelectMultiple)
    ]

    edit_handler = make_translated_interface(
        content_panels=content_panels,
        settings_panels=settings_panels
    )


class InternationalCampaignPage(BasePage):
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

    campaign_subheading = models.CharField(
        max_length=255,
        blank=True,
        help_text="This is a subheading that displays "
                  "when the article is featured on another page"
    )
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

    content_panels = [
        MultiFieldPanel(
            heading='Hero section',
            children=[
                FieldPanel('campaign_heading'),
                FieldPanel('campaign_subheading'),
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
        FieldPanel('title_en_gb'),
        FieldPanel('slug'),
        FieldPanel('tags', widget=CheckboxSelectMultiple)
    ]

    edit_handler = make_translated_interface(
        content_panels=content_panels,
        settings_panels=settings_panels
    )


class InternationalTopicLandingPage(BasePage):
    service_name_value = cms.GREAT_INTERNATIONAL
    parent_page_types = ['great_international.GreatInternationalApp']
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
        FieldPanel('title_en_gb'),
        FieldPanel('slug'),
        FieldPanel('tags', widget=CheckboxSelectMultiple)
    ]

    edit_handler = make_translated_interface(
        content_panels=content_panels,
        settings_panels=settings_panels
    )


class InternationalCuratedTopicLandingPage(BasePage):
    service_name_value = cms.GREAT_INTERNATIONAL
    parent_page_types = ['great_international.GreatInternationalApp']
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
        FieldPanel('title_en_gb'),
        SearchEngineOptimisationPanel(),
        FieldPanel('slug'),
        FieldPanel('tags', widget=CheckboxSelectMultiple)
    ]

    edit_handler = make_translated_interface(
        content_panels=content_panels,
        settings_panels=settings_panels
    )


class InternationalGuideLandingPage(BasePage):
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
        FieldPanel('title_en_gb'),
        SearchEngineOptimisationPanel(),
        FieldPanel('slug'),
        FieldPanel('tags', widget=CheckboxSelectMultiple)
    ]

    edit_handler = make_translated_interface(
        content_panels=content_panels,
        settings_panels=settings_panels
    )


class InternationalCapitalInvestLandingPage(BasePage):
    service_name_value = cms.GREAT_INTERNATIONAL

    @classmethod
    def allowed_subpage_models(cls):
        return [
            CapitalInvestRegionOpportunityPage,
            CapitalInvestSectorOpportunityPage,
            CapitalInvestOpportunityPage
        ]

    parent_page_types = ['great_international.GreatInternationalApp']

    hero_title = models.CharField(max_length=255)
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+', blank=True
    )
    hero_subheading = models.CharField(
        max_length=255,
        blank=True,
        help_text="Please use if you'd like to "
                  "add to the title on a second line"
    )
    hero_subtitle = models.CharField(max_length=255, blank=True)
    hero_cta_text = models.CharField(max_length=255)

    reason_to_invest_section_title = models.CharField(max_length=255)
    reason_to_invest_section_intro = models.CharField(
        max_length=255,
        blank=True
    )
    reason_to_invest_section_content = MarkdownField(blank=True)
    reason_to_invest_section_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+', blank=True
    )
    reason_to_invest_section_image_caption = models.CharField(
        max_length=255,
        blank=True
    )

    region_ops_section_title = models.CharField(
        max_length=255,
        verbose_name="Region opportunities section title"
    )
    region_ops_section_intro = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Region opportunities section intro"
    )

    region_card_one_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+', blank=True
    )
    region_card_one_title = models.CharField(max_length=255)
    region_card_one_description = models.TextField(max_length=255, blank=True)
    region_card_one_cta_text = models.CharField(max_length=255)
    region_card_one_pdf_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    region_card_two_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+', blank=True
    )
    region_card_two_title = models.CharField(max_length=255)
    region_card_two_description = models.TextField(max_length=255, blank=True)
    region_card_two_cta_text = models.CharField(max_length=255)
    region_card_two_pdf_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    region_card_three_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+', blank=True
    )
    region_card_three_title = models.CharField(max_length=255)
    region_card_three_description = models.TextField(max_length=255, blank=True)
    region_card_three_cta_text = models.CharField(max_length=255)
    region_card_three_pdf_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    region_card_four_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+', blank=True
    )
    region_card_four_title = models.CharField(max_length=255)
    region_card_four_description = models.TextField(max_length=255, blank=True)
    region_card_four_cta_text = models.CharField(max_length=255)
    region_card_four_pdf_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    region_card_five_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+', blank=True
    )
    region_card_five_title = models.CharField(max_length=255)
    region_card_five_description = models.TextField(max_length=255, blank=True)
    region_card_five_cta_text = models.CharField(max_length=255)
    region_card_five_pdf_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    region_card_six_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+', blank=True
    )
    region_card_six_title = models.CharField(max_length=255)
    region_card_six_description = models.TextField(max_length=255, blank=True)
    region_card_six_cta_text = models.CharField(max_length=255)
    region_card_six_pdf_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    energy_sector_title = models.CharField(max_length=255)
    energy_sector_content = MarkdownField(blank=True)
    energy_sector_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+', blank=True
    )
    energy_sector_image_caption = models.CharField(max_length=255, blank=True)
    energy_sector_cta_text = models.CharField(max_length=255)
    energy_sector_pdf_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    how_we_help_title = models.CharField(max_length=255)
    how_we_help_intro = models.TextField(max_length=255, blank=True)

    how_we_help_one_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        blank=True
    )
    how_we_help_one_text = models.CharField(max_length=255)

    how_we_help_two_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+', blank=True
    )
    how_we_help_two_text = models.CharField(max_length=255)

    how_we_help_three_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+', blank=True
    )
    how_we_help_three_text = models.CharField(max_length=255)

    how_we_help_four_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+', blank=True
    )
    how_we_help_four_text = models.CharField(max_length=255)

    contact_section_title = models.CharField(max_length=255)
    contact_section_text = models.CharField(max_length=255, blank=True)
    contact_section_cta_text = models.CharField(max_length=255)

    tags = ParentalManyToManyField(Tag, blank=True)
    content_panels = [
        MultiFieldPanel(
            heading="Hero",
            children=[
                ImageChooserPanel('hero_image'),
                FieldPanel('hero_title'),
                FieldPanel('hero_subheading'),
                FieldPanel('hero_subtitle'),
                FieldPanel('hero_cta_text')
            ]
        ),
        MultiFieldPanel(
            heading="Reason to invest in the UK section",
            children=[
                FieldPanel('reason_to_invest_section_title'),
                FieldPanel('reason_to_invest_section_intro'),
                FieldPanel('reason_to_invest_section_content'),
                FieldPanel('reason_to_invest_section_image_caption'),
                ImageChooserPanel('reason_to_invest_section_image')
            ]
        ),
        MultiFieldPanel(
            heading="Investment Opportunities by regions",
            children=[
                FieldPanel('region_ops_section_title'),
                FieldPanel('region_ops_section_intro'),
                FieldRowPanel([
                    MultiFieldPanel([
                        ImageChooserPanel('region_card_one_image'),
                        FieldPanel('region_card_one_title'),
                        FieldPanel('region_card_one_description'),
                        FieldPanel('region_card_one_cta_text'),
                        DocumentChooserPanel('region_card_one_pdf_document'),
                    ]),
                    MultiFieldPanel([
                        ImageChooserPanel('region_card_two_image'),
                        FieldPanel('region_card_two_title'),
                        FieldPanel('region_card_two_description'),
                        FieldPanel('region_card_two_cta_text'),
                        DocumentChooserPanel('region_card_two_pdf_document'),
                    ]),
                    MultiFieldPanel([
                        ImageChooserPanel('region_card_three_image'),
                        FieldPanel('region_card_three_title'),
                        FieldPanel('region_card_three_description'),
                        FieldPanel('region_card_three_cta_text'),
                        DocumentChooserPanel('region_card_three_pdf_document'),
                    ]),
                ]),
                FieldRowPanel([
                    MultiFieldPanel([
                        ImageChooserPanel('region_card_four_image'),
                        FieldPanel('region_card_four_title'),
                        FieldPanel('region_card_four_description'),
                        FieldPanel('region_card_four_cta_text'),
                        DocumentChooserPanel('region_card_four_pdf_document'),
                    ]),
                    MultiFieldPanel([
                        ImageChooserPanel('region_card_five_image'),
                        FieldPanel('region_card_five_title'),
                        FieldPanel('region_card_five_description'),
                        FieldPanel('region_card_five_cta_text'),
                        DocumentChooserPanel('region_card_five_pdf_document'),
                    ]),
                    MultiFieldPanel([
                        ImageChooserPanel('region_card_six_image'),
                        FieldPanel('region_card_six_title'),
                        FieldPanel('region_card_six_description'),
                        FieldPanel('region_card_six_cta_text'),
                        DocumentChooserPanel('region_card_six_pdf_document'),
                    ]),
                ]),
            ]
        ),
        MultiFieldPanel(
            heading="Energy Sector",
            children=[
                FieldPanel('energy_sector_title'),
                FieldPanel('energy_sector_content'),
                ImageChooserPanel('energy_sector_image'),
                FieldPanel('energy_sector_image_caption'),
                FieldPanel('energy_sector_cta_text'),
                DocumentChooserPanel('energy_sector_pdf_document'),
            ]
        ),
        MultiFieldPanel(
            heading="How we help section",
            children=[
                FieldPanel('how_we_help_title'),
                FieldPanel('how_we_help_intro'),
                FieldRowPanel([
                    MultiFieldPanel([
                        ImageChooserPanel('how_we_help_one_icon'),
                        FieldPanel('how_we_help_one_text'),
                    ]),
                    MultiFieldPanel([
                        ImageChooserPanel('how_we_help_two_icon'),
                        FieldPanel('how_we_help_two_text'),
                    ]),
                ]),
                FieldRowPanel([
                    MultiFieldPanel([
                        ImageChooserPanel('how_we_help_three_icon'),
                        FieldPanel('how_we_help_three_text'),
                    ]),
                    MultiFieldPanel([
                        ImageChooserPanel('how_we_help_four_icon'),
                        FieldPanel('how_we_help_four_text'),
                    ]),
                ]),
            ]
        ),
        MultiFieldPanel(
            heading="Contact Section",
            children=[
                FieldPanel('contact_section_title'),
                FieldPanel('contact_section_text'),
                FieldPanel('contact_section_cta_text')
            ]
        ),
    ]

    settings_panels = [
        FieldPanel('title_en_gb'),
        FieldPanel('slug'),
        FieldPanel('tags', widget=CheckboxSelectMultiple)
    ]

    edit_handler = make_translated_interface(
        content_panels=content_panels,
        settings_panels=settings_panels
    )


class CapitalInvestRegionOpportunityPage(BasePage):
    service_name_value = cms.GREAT_INTERNATIONAL

    @classmethod
    def allowed_subpage_models(cls):
        return [
            CapitalInvestSectorOpportunityPage,
            CapitalInvestOpportunityPage
        ]

    parent_page_types = [
        'great_international.InternationalCapitalInvestLandingPage',
        'great_international.CapitalInvestSectorOpportunityPage']

    breadcrumbs_label = models.CharField(max_length=255)
    hero_title = models.CharField(max_length=255)
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        blank=True
    )

    region_summary_section_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        blank=True
    )
    region_summary_section_intro = models.TextField(max_length=255)
    region_summary_section_content = MarkdownField(blank=True)

    investment_opps_title = models.CharField(
        max_length=255,
        verbose_name="Investment opportunities title"
    )
    investment_opps_intro = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Investment opportunities intro"
    )

    economics_data_title = models.CharField(max_length=255, blank=True)
    economics_stats_number_1 = models.CharField(max_length=255, blank=True)
    economics_stats_heading_1 = models.CharField(max_length=255, blank=True)
    economics_stats_smallprint_1 = models.CharField(max_length=255, blank=True)

    economics_stats_number_2 = models.CharField(max_length=255, blank=True)
    economics_stats_heading_2 = models.CharField(max_length=255, blank=True)
    economics_stats_smallprint_2 = models.CharField(max_length=255, blank=True)

    economics_stats_number_3 = models.CharField(max_length=255, blank=True)
    economics_stats_heading_3 = models.CharField(max_length=255, blank=True)
    economics_stats_smallprint_3 = models.CharField(max_length=255, blank=True)

    economics_stats_number_4 = models.CharField(max_length=255, blank=True)
    economics_stats_heading_4 = models.CharField(max_length=255, blank=True)
    economics_stats_smallprint_4 = models.CharField(max_length=255, blank=True)

    location_data_title = models.CharField(
        max_length=255,
        blank=True
    )
    location_stats_number_1 = models.CharField(
        max_length=255,
        blank=True
    )
    location_stats_heading_1 = models.CharField(
        max_length=255,
        blank=True
    )
    location_stats_smallprint_1 = models.CharField(
        max_length=255,
        blank=True
    )

    location_stats_number_2 = models.CharField(
        max_length=255,
        blank=True
    )
    location_stats_heading_2 = models.CharField(
        max_length=255,
        blank=True
    )
    location_stats_smallprint_2 = models.CharField(
        max_length=255,
        blank=True
    )

    location_stats_number_3 = models.CharField(
        max_length=255,
        blank=True
    )
    location_stats_heading_3 = models.CharField(
        max_length=255,
        blank=True
    )
    location_stats_smallprint_3 = models.CharField(
        max_length=255,
        blank=True
    )

    location_stats_number_4 = models.CharField(
        max_length=255,
        blank=True
    )
    location_stats_heading_4 = models.CharField(
        max_length=255,
        blank=True
    )
    location_stats_smallprint_4 = models.CharField(
        max_length=255,
        blank=True
    )

    section_title = models.CharField(max_length=255, blank=True)
    section_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        blank=True
    )
    section_content = MarkdownField(blank=True)

    case_study_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        blank=True
    )
    case_study_title = models.CharField(max_length=255)
    case_study_text = models.TextField(max_length=255, blank=True)
    case_study_cta_text = models.CharField(max_length=255)
    case_study_cta_link = models.CharField(max_length=255, blank=True)

    next_steps_title = models.CharField(max_length=255)
    next_steps_intro = models.TextField(max_length=255, blank=True)

    invest_cta_text = models.CharField(max_length=255)
    invest_cta_link = models.CharField(max_length=255, blank=True)

    buy_cta_text = models.CharField(max_length=255)
    buy_cta_link = models.CharField(max_length=255, blank=True)

    tags = ParentalManyToManyField(Tag, blank=True)

    content_panels = [
        FieldPanel('breadcrumbs_label'),
        MultiFieldPanel(
            heading="Hero",
            children=[
                FieldPanel('hero_title'),
                ImageChooserPanel('hero_image'),
            ],
        ),
        MultiFieldPanel(
            heading="Region summary",
            children=[
                ImageChooserPanel('region_summary_section_image'),
                FieldPanel('region_summary_section_intro'),
                FieldPanel('region_summary_section_content'),
            ],
        ),
        MultiFieldPanel(
            heading="Investment opportunities",
            children=[
                FieldPanel('investment_opps_title'),
                FieldPanel('investment_opps_intro'),
            ]
        ),
        MultiFieldPanel(
            heading="Economics Statistics",
            children=[
                FieldPanel('economics_data_title'),
                FieldRowPanel([
                    MultiFieldPanel([
                        FieldPanel('economics_stats_number_1'),
                        FieldPanel('economics_stats_heading_1'),
                        FieldPanel('economics_stats_smallprint_1'),
                    ]),
                    MultiFieldPanel([
                        FieldPanel('economics_stats_number_2'),
                        FieldPanel('economics_stats_heading_2'),
                        FieldPanel('economics_stats_smallprint_2'),
                    ]),
                    MultiFieldPanel([
                        FieldPanel('economics_stats_number_3'),
                        FieldPanel('economics_stats_heading_3'),
                        FieldPanel('economics_stats_smallprint_3'),
                    ]),
                    MultiFieldPanel([
                        FieldPanel('economics_stats_number_4'),
                        FieldPanel('economics_stats_heading_4'),
                        FieldPanel('economics_stats_smallprint_4'),
                    ]),
                ]),
            ],
        ),
        MultiFieldPanel(
            heading="Location Statistics",
            children=[
                FieldPanel('location_data_title'),
                FieldRowPanel([
                    MultiFieldPanel([
                        FieldPanel('location_stats_number_1'),
                        FieldPanel('location_stats_heading_1'),
                        FieldPanel('location_stats_smallprint_1'),
                    ]),
                    MultiFieldPanel([
                        FieldPanel('location_stats_number_2'),
                        FieldPanel('location_stats_heading_2'),
                        FieldPanel('location_stats_smallprint_2'),
                    ]),
                    MultiFieldPanel([
                        FieldPanel('location_stats_number_3'),
                        FieldPanel('location_stats_heading_3'),
                        FieldPanel('location_stats_smallprint_3'),
                    ]),
                    MultiFieldPanel([
                        FieldPanel('location_stats_number_4'),
                        FieldPanel('location_stats_heading_4'),
                        FieldPanel('location_stats_smallprint_4'),
                    ]),
                ]),
            ],
        ),
        MultiFieldPanel(
            heading="Extra optional section",
            children=[
                ImageChooserPanel('section_image'),
                FieldPanel('section_title'),
                FieldPanel('section_content'),
            ],
        ),
        MultiFieldPanel(
            heading="Case study",
            children=[
                ImageChooserPanel('case_study_image'),
                FieldPanel('case_study_title'),
                FieldPanel('case_study_text'),
                FieldPanel('case_study_cta_text'),
                FieldPanel('case_study_cta_link'),
            ],
        ),
        MultiFieldPanel(
            heading="Next steps",
            children=[
                FieldPanel('next_steps_title'),
                FieldPanel('next_steps_intro'),
                FieldRowPanel([
                    MultiFieldPanel([
                        FieldPanel('invest_cta_text'),
                        FieldPanel('invest_cta_link'),
                    ]),
                    MultiFieldPanel([
                        FieldPanel('buy_cta_text'),
                        FieldPanel('buy_cta_link'),
                    ]),
                ]),
            ],
        ),
    ]

    settings_panels = [
        FieldPanel('title_en_gb'),
        FieldPanel('slug'),
        FieldPanel('tags', widget=CheckboxSelectMultiple)
    ]

    edit_handler = make_translated_interface(
        content_panels=content_panels,
        settings_panels=settings_panels
    )


class CapitalInvestSectorOpportunityPage(BasePage):
    service_name_value = cms.GREAT_INTERNATIONAL

    @classmethod
    def allowed_subpage_models(cls):
        return [
            CapitalInvestOpportunityPage,
            CapitalInvestRegionOpportunityPage,
        ]

    parent_page_types = [
        'great_international.CapitalInvestRegionOpportunityPage',
        'great_international.InternationalCapitalInvestLandingPage']

    breadcrumbs_label = models.CharField(max_length=255)
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        blank=True
    )
    hero_title = models.CharField(max_length=255)
    featured_description = models.TextField(
        max_length=255,
        blank=True,
        help_text="This description is used when this page is featured "
                  "on another page, i.e. the Capital Invest Region "
                  "Opportunities page"
    )

    sector_summary_intro = models.TextField(max_length=255, blank=True)
    sector_summary_content = MarkdownField(blank=True)
    sector_summary_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        blank=True
    )

    investment_opportunities_title = models.CharField(max_length=255)

    next_steps_title = models.CharField(max_length=255)
    next_steps_intro = models.CharField(max_length=255, blank=True)

    invest_cta_text = models.CharField(max_length=255)
    invest_cta_link = models.CharField(max_length=255, blank=True)
    buy_cta_text = models.CharField(max_length=255)
    buy_cta_link = models.CharField(max_length=255, blank=True)

    tags = ParentalManyToManyField(Tag, blank=True)

    content_panels = [
        FieldPanel('breadcrumbs_label'),
        MultiFieldPanel(
            heading="Hero",
            children=[
                ImageChooserPanel('hero_image'),
                FieldPanel('hero_title'),
            ],
        ),
        FieldPanel('featured_description'),
        MultiFieldPanel(
            heading="Sector summary",
            children=[
                FieldPanel('sector_summary_intro'),
                FieldPanel('sector_summary_content'),
                ImageChooserPanel('sector_summary_image'),
            ],
        ),
        FieldPanel('investment_opportunities_title'),
        MultiFieldPanel(
            heading="Next steps",
            children=[
                FieldPanel('next_steps_title'),
                FieldPanel('next_steps_intro'),
                FieldRowPanel([
                    MultiFieldPanel([
                        FieldPanel('invest_cta_text'),
                        FieldPanel('invest_cta_link'),
                    ]),
                    MultiFieldPanel([
                        FieldPanel('buy_cta_text'),
                        FieldPanel('buy_cta_link'),
                    ]),
                ]),
            ],
        ),
    ]

    settings_panels = [
        FieldPanel('title_en_gb'),
        FieldPanel('slug'),
        FieldPanel('tags', widget=CheckboxSelectMultiple)
    ]

    edit_handler = make_translated_interface(
        content_panels=content_panels,
        settings_panels=settings_panels
    )


class CapitalInvestOpportunityPage(BasePage):
    service_name_value = cms.GREAT_INTERNATIONAL

    parent_page_types = [
        'great_international.CapitalInvestSectorOpportunityPage',
        'great_international.CapitalInvestRegionOpportunityPage']

    breadcrumbs_label = models.CharField(max_length=255)
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        blank=True
    )
    hero_title = models.CharField(max_length=255)

    opportunity_summary_intro = models.TextField(max_length=255)
    opportunity_summary_content = MarkdownField(blank=True)
    opportunity_summary_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        blank=True
    )

    location = models.CharField(max_length=255)
    project_promoter = models.CharField(max_length=255)
    scale = models.CharField(max_length=255)
    programme = models.CharField(max_length=255)
    investment_type = models.CharField(max_length=255)
    planning_status = models.CharField(max_length=255)

    project_background_title = models.CharField(max_length=255, blank=True)
    project_background_intro = models.TextField(max_length=255, blank=True)
    project_description_title = models.CharField(max_length=255, blank=True)
    project_description_content = MarkdownField(blank=True)
    project_promoter_title = models.CharField(max_length=255, blank=True)
    project_promoter_content = MarkdownField(blank=True)
    project_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        blank=True
    )

    case_study_title = models.CharField(max_length=255)
    case_study_text = models.CharField(max_length=255, blank=True)
    case_study_cta_text = models.CharField(max_length=255)
    case_study_cta_link = models.CharField(max_length=255, blank=True)
    case_study_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        blank=True
    )

    similar_projects_title = models.CharField(max_length=255)
    similar_projects_cta_text = models.CharField(max_length=255)
    similar_projects_cta_link = models.CharField(max_length=255, blank=True)

    next_steps_title = models.CharField(max_length=255)
    next_steps_intro = models.CharField(max_length=255, blank=True)

    invest_cta_text = models.CharField(max_length=255)
    invest_cta_link = models.CharField(max_length=255, blank=True)
    buy_cta_text = models.CharField(max_length=255)
    buy_cta_link = models.CharField(max_length=255, blank=True)

    tags = ParentalManyToManyField(Tag, blank=True)

    content_panels = [
        FieldPanel('breadcrumbs_label'),
        MultiFieldPanel(
            heading="Hero",
            children=[
                ImageChooserPanel('hero_image'),
                FieldPanel('hero_title'),
            ],
        ),
        MultiFieldPanel(
            heading="Opportunity summary",
            children=[
                FieldPanel('opportunity_summary_intro'),
                FieldPanel('opportunity_summary_content'),
                ImageChooserPanel('opportunity_summary_image'),
            ],
        ),
        MultiFieldPanel(
            heading="Opportunity Details",
            children=[
                FieldRowPanel([
                    FieldPanel('location'),
                    FieldPanel('project_promoter'),
                    FieldPanel('scale'),
                ]),
                FieldRowPanel([
                    FieldPanel('programme'),
                    FieldPanel('investment_type'),
                    FieldPanel('planning_status'),
                ]),
            ],
        ),
        MultiFieldPanel(
            heading="Project Details",
            children=[
                FieldPanel('project_background_title'),
                FieldPanel('project_background_intro'),
                FieldRowPanel([
                    MultiFieldPanel([
                        FieldPanel('project_description_title'),
                        FieldPanel('project_description_content'),
                    ]),
                    MultiFieldPanel([
                        FieldPanel('project_promoter_title'),
                        FieldPanel('project_promoter_content'),
                    ]),
                ]),
                ImageChooserPanel('project_image')
            ],
        ),
        MultiFieldPanel(
            heading="Case study",
            children=[
                ImageChooserPanel('case_study_image'),
                FieldPanel('case_study_title'),
                FieldPanel('case_study_cta_text'),
                FieldPanel('case_study_cta_link'),
            ],
        ),
        MultiFieldPanel(
            heading="Similar projects",
            children=[
                FieldPanel('similar_projects_title'),
                FieldPanel('similar_projects_cta_text'),
                FieldPanel('similar_projects_cta_link'),
            ],
        ),
        MultiFieldPanel(
            heading="Next steps",
            children=[
                FieldPanel('next_steps_title'),
                FieldPanel('next_steps_intro'),
                FieldRowPanel([
                    MultiFieldPanel([
                        FieldPanel('invest_cta_text'),
                        FieldPanel('invest_cta_link'),
                    ]),
                    MultiFieldPanel([
                        FieldPanel('buy_cta_text'),
                        FieldPanel('buy_cta_link'),
                    ]),
                ]),
            ],
        ),
    ]

    settings_panels = [
        FieldPanel('title_en_gb'),
        FieldPanel('slug'),
        FieldPanel('tags', widget=CheckboxSelectMultiple)
    ]

    edit_handler = make_translated_interface(
        content_panels=content_panels,
        settings_panels=settings_panels
    )
