from django.conf import settings
from django.db import models


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
