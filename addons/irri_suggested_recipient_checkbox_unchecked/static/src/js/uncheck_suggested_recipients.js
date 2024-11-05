/** @odoo-module **/

document.addEventListener('DOMContentLoaded', function () {
    function uncheckSuggestedRecipients() {
        document.querySelectorAll('.o-mail-SuggestedRecipient .form-check-input').forEach(function (checkbox) {
            checkbox.checked = false;
        });
    }

    // Run the function on page load
    uncheckSuggestedRecipients();

    // Observe changes in the DOM to handle dynamic additions
    const observer = new MutationObserver(function (mutations) {
        mutations.forEach(function () {
            uncheckSuggestedRecipients();
        });
    });

    observer.observe(document.body, { childList: true, subtree: true });
});
