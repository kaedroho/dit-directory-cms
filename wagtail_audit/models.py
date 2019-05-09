import json

from django.conf import settings
from django.db import models
from django.utils.functional import cached_property


class PageActionLogEntry(models.Model):
    page = models.ForeignKey('wagtailcore.Page', on_delete=models.SET_NULL, null=True, related_name='action_log_entries')
    revision = models.ForeignKey('wagtailcore.PageRevision', on_delete=models.SET_NULL, null=True, related_name='+')
    action = models.CharField(max_length=255)
    data = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    time = models.DateTimeField()

    # Flags
    created = models.BooleanField(default=False)
    content_changed = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    unpublished = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    @property
    def verbs(self):
        verbs = []

        if self.created:
            verbs.append("created")
        elif self.content_changed:
            verbs.append("edited")

        if self.published:
            verbs.append("published")

        if self.deleted:
            verbs.append("deleted")
        elif self.unpublished:
            verbs.append("unpublished")

        if len(verbs) > 0:
            lastverb = verbs[-1]
            verbs = verbs[:-1]

            if verbs:
                lastverb = ' and ' + lastverb

            return ', '.join(verbs) + lastverb

        else:
            return ''

    @cached_property
    def data_json(self):
        if self.data:
            return json.loads(self.data)
        else:
            return {}
