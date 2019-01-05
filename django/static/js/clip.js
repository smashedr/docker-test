// This will work on any pate with out ajax

// Document Dot Ready
$(document).ready(function() {

    // Init a Clipboard for .copy-data and preventDefault
    new Clipboard('.copy-data');
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
