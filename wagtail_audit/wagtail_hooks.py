import json

from django.conf.urls import url, include
from django.templatetags.static import static
from django.utils import timezone
from django.utils.html import format_html, format_html_join

from wagtail.core import hooks

from . import views
from .models import PageActionLogEntry


@hooks.register('register_admin_urls')
def register_admin_urls():
    urls = [
        url('^logs/page/(\d+)/$', views.page_history, name='page_history'),
    ]

    return [
        url('^audit/', include((urls, 'wagtail_audit'), namespace='wagtail_audit')),
    ]


@hooks.register('insert_editor_js')
def editor_js():
    js_files = [
        'wagtail_audit/page-editor-plugin.js',
    ]
    js_includes = format_html_join('\n', '<script src="{0}"></script>',
        ((static(filename),) for filename in js_files)
    )
    return js_includes


def page_info(page):
    return {
        'id': page.id,
        'title': page.get_admin_display_title(),
        'slug': page.slug,
        'url_path': page.url_path,
    }


@hooks.register('after_create_page', order=-1)
def after_create_page(request, page):
    PageActionLogEntry.objects.create(
        page=page,
        revision=page.get_latest_revision(),
        action='create',
        data=json.dumps({
            'page': page_info(page),
        }),
        user=request.user,
        time=timezone.now(),
        created=True,
        published=page.live,
    )


@hooks.register('after_edit_page', order=-1)
def after_edit_page(request, page):
    if bool(request.POST.get('action-submit')):
        action = 'submit-for-moderation'
    elif bool(request.POST.get('revision')):
        action = 'revert'
    elif bool(request.POST.get('action-publish')):
        action = 'publish'
    else:
        action = 'save-draft'

    # Check if anything has changed
    revision = page.get_latest_revision()
    previous_revision = revision.get_previous()
    revision_content = json.loads(revision.content_json)
    previous_revision_content = json.loads(revision.content_json)
    for ignored_field in ['live', 'has_unpublished_changes', 'url_path', 'path', 'depth', 'numchild', 'latest_revision_created_at', 'live_revision', 'draft_title', 'owner', 'locked']:
        del revision_content[ignored_field]
        del previous_revision_content[ignored_field]
    content_changed = revision_content != previous_revision_content

    data = {
        'page': page_info(page),
    }

    if content_changed:
        # Comment must be set if content has changed, or crash
        # TODO: Replace this with a nice error message. That must be raised
        # from before_edit_page though
        data['comment'] = request.POST['wagtailaudit_comment']

    PageActionLogEntry.objects.create(
        page=page,
        revision=page.get_latest_revision(),
        action=action,
        data=json.dumps(data),
        user=request.user,
        time=timezone.now(),
        content_changed=content_changed,
        published=action == 'publish',
    )


@hooks.register('after_delete_page', order=-1)
def after_delete_page(request, page):
    PageActionLogEntry.objects.create(
        page=page,
        action='delete',
        data=json.dumps({
            'page': page_info(page),
        }),
        user=request.user,
        time=timezone.now(),
        deleted=True,
        unpublished=page.live,
    )


@hooks.register('after_copy_page', order=-1)
def after_copy_page(request, from_page, new_page):
    PageActionLogEntry.objects.create(
        page=new_page,
        revision=page.get_latest_revision(),
        action='copy',
        data=json.dumps({
            'page': page_info(page),
            'copied_from': page_info(from_page),
            'new_parent': page_info(new_page.get_parent()),
        }),
        user=request.user,
        time=timezone.now(),
        created=True,
        published=new_page.live,
    )


@hooks.register('after_move_page', order=-1)
def after_move_page(request, page):
    PageActionLogEntry.objects.create(
        page=page,
        action='move',
        data=json.dumps({
            'page': page_info(page),
            'new_parent': page_info(page.get_parent()),
        }),
        user=request.user,
        time=timezone.now(),
    )


# TODO: Reject/approve moderation
# TODO: Unpublish
# TODO: Publish by scheduled task
