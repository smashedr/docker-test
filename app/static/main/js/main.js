// DoC U MenT DoT ReaD Y
$(document).ready(function() {

    // Log Out Form Activator Button
    $('.log-out').click(function () {
        $('#log-out').submit();
        return false;
    });

    // Every time a modal is shown, if it has an autofocus element, focus on it.
    $('.modal').on('shown.bs.modal', function() {
        $(this).find('[autofocus]').focus();
    });

});
