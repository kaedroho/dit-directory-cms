from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from wagtail.admin.utils import user_has_any_page_permission, user_passes_test
from wagtail.core.models import Page
from wagtail.utils.pagination import paginate

from .models import PageActionLogEntry


def get_comparison(page, revision_a, revision_b):
    comparison = page.get_edit_handler().get_comparison()
    comparison = [comp(revision_a, revision_b) for comp in comparison]
    comparison = [comp for comp in comparison if comp.has_changed()]

    return comparison


@user_passes_test(user_has_any_page_permission)
def log_entry(request, page_id, log_entry_id):
    page = get_object_or_404(Page, id=page_id)
    log_entry = get_object_or_404(page.action_log_entries.all(), id=log_entry_id)

    if log_entry.content_changed:
        previous_log_entry = page.action_log_entries.filter(content_changed=True, time__lt=log_entry.time).order_by('-time').first()
        comparison = get_comparison(page, previous_log_entry.revision.as_page_object(), log_entry.revision.as_page_object())
    else:
        comparison = None

    return render(request, 'wagtail_audit/log_entry.html', {
        'page': page,
        'log_entry': log_entry,
        'comparison': comparison,
    })


@user_passes_test(user_has_any_page_permission)
def page_history(request, page_id):
    page = get_object_or_404(Page, id=page_id)

    log_entries = list(page.action_log_entries.order_by('time'))

    previous_changed = None
    for log_entry in log_entries:
        log_entry.previous_changed = previous_changed

        if log_entry.created or log_entry.content_changed:
            previous_changed = log_entry

    log_entries.reverse()

    return render(request, 'wagtail_audit/page_history.html', {
        'page': page,
        'log_entries': log_entries,
    })


@user_passes_test(user_has_any_page_permission)
def site_history(request):
    log_entries = PageActionLogEntry.objects.order_by('-time')
    paginator, log_entries = paginate(request, log_entries, per_page=50)

    return render(request, 'wagtail_audit/site_history.html', {
        'paginator': paginator,
        'log_entries': log_entries,
    })
