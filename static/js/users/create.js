$(document).ready(function() {
    $('#save-button').on('click', function() {
        var succes_form = document.getElementById('create-form').checkValidity();
        console.log(succes_form);
        if (succes_form) {
            showModal(
                'bx bxs-save',
                'Confirmación',
                '¿Estás seguro de que deseas guardar este registro?',
                'No', 
                'close', 
                'Sí, guardar', 
                function() { $('#create-form').submit(); }
            );
        } else {
            $('#create-form').addClass('was-validated');
        }
    });
});