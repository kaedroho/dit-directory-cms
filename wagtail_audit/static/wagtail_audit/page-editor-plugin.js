function askForComment(submit) {
    // TODO: Don't show if only publishing/submitting and no changes have been made
    let comment = prompt("Please enter a comment to describe the changes you have made");

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

        fn(submit);

        e.preventDefault();
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
});
