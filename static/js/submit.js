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
        'fas fa-info', // iconClass
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
                if (!data.hasOwnProperty('error')) {
                    callback();
                    return false;
                }
                message_error(data.error);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {

            });
        }
    );
}