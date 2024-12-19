$(document).ready(function() {
    // Inicializar el datatable con id scroll-horizontal, con el idioma y textos en español
    $('#scroll-horizontal').DataTable({
        scrollX: true,
        responsive: true,
        autowidth: false,
        language: {
            url: languageUrl
        }
    });

    // Manejar el evento de clic del botón de actualizar
    $('#updateButton').on('click', function() {
        $('#spinner').removeClass('d-none');

        $.ajax({
            url: updateUrl,
            type: 'POST',
            data: {
                id: 1
            },
            dataType: 'json',
            success: function(response) {
                
                setTimeout(function() {
                    $('#spinner').addClass('d-none');
                });
                
                $('#scroll-horizontal').DataTable().ajax.reload();
            },
            error: function(error) {
                console.log(error);
            }
        });

    });

});