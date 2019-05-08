from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from wagtail.admin.utils import user_has_any_page_permission, user_passes_test
from wagtail.core.models import Page
from wagtail.utils.pagination import paginate


@user_passes_test(user_has_any_page_permission)
def page_history(request, page_id):
    page = get_object_or_404(Page, id=page_id).specific

    # Get page ordering
    ordering = request.GET.get('ordering', '-time')
    if ordering not in ['time', '-time', ]:
        ordering = '-time'

    log_entries = list(page.action_log_entries.order_by(ordering))

    previous_changed = None
    for log_entry in log_entries:
        log_entry.previous_changed = previous_changed

        if log_entry.content_changed:
            previous_changed = log_entry

    paginator, log_entries = paginate(request, log_entries)

    return render(request, 'wagtail_audit/page_history.html', {
        'page': page,
        'ordering': ordering,
        'pagination_query_params': "ordering=%s" % ordering,
        'log_entries': log_entries,
    })
