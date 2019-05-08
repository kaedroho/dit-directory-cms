import json

from django.utils import timezone

from wagtail.core import hooks

from .models import PageActionLogEntry


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

    PageActionLogEntry.objects.create(
        page=page,
        revision=page.get_latest_revision(),
        action=action,
        data=json.dumps({
            'page': page_info(page),
        }),
        user=request.user,
        time=timezone.now(),
        content_changed=True,  # TODO: are there any changes made?
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
