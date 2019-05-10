import json

from django.core.management.base import BaseCommand, CommandError
from wagtail.core.models import PageRevision

from wagtail_audit.models import PageActionLogEntry


class Command(BaseCommand):
    def handle(self, *args, **options):
        current_page_id = None

        revisions_that_were_once_live = set()
        for revision in PageRevision.objects.order_by('page_id', 'created_at').select_related('page').iterator():
            new_page = revision.page_id != current_page_id
            current_page_id = revision.page_id
            if new_page:
                previous_revision_content = None

            content = json.loads(revision.content_json)

            if content.get('live_revision'):
                revisions_that_were_once_live.add(content['live_revision'])

            for ignored_field in ['live', 'has_unpublished_changes', 'url_path', 'path', 'depth', 'numchild', 'latest_revision_created_at', 'live_revision', 'draft_title', 'owner', 'locked']:
                del content[ignored_field]

            if not PageActionLogEntry.objects.filter(revision=revision).exists():
                content_changed = not new_page and previous_revision_content != content
                published = revision.id == revision.page.live_revision_id

                if content_changed or published:
                    PageActionLogEntry.objects.create(
                        page_id=revision.page_id,
                        revision=revision,
                        action='converted-revision',
                        data='',
                        user=revision.user,
                        time=revision.created_at,
                        created=new_page,
                        content_changed=content_changed,
                        published=revision.id == revision.page.live_revision_id,
                    )

            previous_revision_content = content

        PageActionLogEntry.objects.filter(action='converted-revision', revision_id__in=revisions_that_were_once_live, published=False).update(published=True)
