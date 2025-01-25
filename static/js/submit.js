function message_error(obj) {
    var html = '';
    if (typeof (obj) === 'object') {
        html = '<ul style="text-align: left;">';
        $.each(obj, function (key, value) {
            html += '<li>' + key + ': ' + value + '</li>';
        });
        html += '</ul>';
    } else {
        html = '<p>' + obj + '</p>';
    }
    Swal.fire({
        title: 'Error!',
        html: html,
        icon: 'error'
    });
}

function submit_with_ajax(url, title, content, parameters, callback) {
    console.log('Parameters before AJAX call:', parameters);
    showModal(
        'bx bxs-save', // iconClass
        title, // title
        content, // message
        'Cancelar', // button1Text
        'close', // button1Action
        'Confirmar', // button2Text
        function() { // button2Action
            $.ajax({
                url: url, //window.location.pathname
                type: 'POST',
                data: $.param(parameters), // Serialize parameters
                contentType: 'application/x-www-form-urlencoded; charset=UTF-8', // Set content type to URL encoded
                processData: true,
                dataType: 'json'
            }).done(function (data) {
                console.log(data);
                // cerrar modal 
                if (!data.hasOwnProperty('error')) {
                    callback(data);
                    return false;
                }
                message_error(data.error);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {

            });
        },
        colorIcon="#25a0e2",
        id="ajax_modal", 
        id_button_1="button1_ajax", 
        id_button_2="button2_ajax"
    );
}