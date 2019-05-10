function askForComment(submit, cancel) {
    // TODO: Don't show if only publishing/submitting and no changes have been made
    let comment = null;
    while (!comment) {
        comment = prompt("Please enter a comment to describe the changes you have made");

        if (comment === null) {
            // User pressed cancel
            cancel();
            return;
        }
    }

    let commentInput = document.createElement('input');
    commentInput.type = 'hidden';
    commentInput.name = 'wagtailaudit_comment';
    commentInput.value = comment;

    let form = document.getElementById('page-edit-form');
    form.appendChild(commentInput);

    submit();
}

function interceptClickEvent(element, fn) {
    let eventListener = e => {
        let submit = () => {
            element.removeEventListener('click', eventListener);

            let event = new MouseEvent('click', {
                view: window,
                bubbles: true,
                cancelable: true
            });
            element.dispatchEvent(event);
        };

        let cancel = () => {
            // Don't let wagtail see that this button was clicked
            e.stopImmediatePropagation();
        };

        fn(submit, cancel);

        e.preventDefault();

        return false;
    };

    element.addEventListener('click', eventListener);
}

document.addEventListener('DOMContentLoaded', () => {
    let form = document.getElementById('page-edit-form');
    let saveDraftButton = document.querySelector('button.action-save');
    let publishButton = document.querySelector('button[name="action-publish"]');
    let submitButton = document.querySelector('input[name="action-submit"]');

    window.wagtailAuditInitialFormData = $(form).serialize();

    interceptClickEvent(saveDraftButton, askForComment);
    interceptClickEvent(publishButton, askForComment);
    interceptClickEvent(submitButton, askForComment);

    // HACK: Replace "Revisions" with "History"
    let revisionsLink = document.querySelector('footer .meta > .modified a');
    if (revisionsLink) {
        revisionsLink.innerHTML = 'History';
        revisionsLink.href = revisionsLink.href.replace('/admin/pages/', '/admin/audit/logs/page/').replace('/revisions/', '/');
    }
});
