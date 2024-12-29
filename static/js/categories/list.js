$(document).ready(function() {
    // Inicializar el datatable con id scroll-horizontal, con el idioma y textos en español
    $('#scroll-horizontal').DataTable({
        scrollX: true,
        responsive: true,
        autowidth: false,
        order: [[1, 'asc']], // Ordena por la segunda columna (índice 1) en orden ascendente
        language: {
            url: languageUrl
        }
    });
});