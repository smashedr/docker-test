//
// this is not used and the ajax end point does not exist
//

$(document).ready(function() {

    $('#login').on('submit', function(event){

        event.preventDefault();

        if ($('#login-button').hasClass('disabled')) {
            return;
        }

        var formData = new FormData($(this)[0]);

        $.ajax({
            url: '/login/ajax/',
            type: 'POST',
            data: formData,
            beforeSend: function( jqXHR ){
                $('#login-button').addClass('disabled');
            },
            complete: function(){
                $('#login-button').removeClass('disabled');
            },
            success: function(data, textStatus, jqXHR){
                console.log("Status: "+textStatus+" Data: "+data);
                // redirect to next_url

            },
            error: function(data, textStatus, errorThrown) {
                console.log("Status: "+textStatus+" Data: "+data.responseText);
                // show login error

            },
            cache: false,
            contentType: false,
            processData: false
        });

        return false;

    });

});
