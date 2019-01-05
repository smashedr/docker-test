// DoC U MenT DoT ReaD Y
$(document).ready(function() {

    // Init a Clipboard for .copy-data and preventDefault
    new ClipboardJS('.copy-data');
    $( ".copy-data" ).click(function( event ) {
        event.preventDefault();
    });

    // pop er up er time er out er
    $('.pop').popover({html:true}).click(function () {
        setTimeout(function () {
            $('.pop').popover('hide');
        }, 1000);
    });

});
