$(document).ready(function() {

    var tblSale = $('#scroll-horizontal').DataTable({
        scrollX: true,
        responsive: true,
        autowidth: false,
        order: [[1, 'asc']],
        // Configuración de DataTables
        columns: [
            { data: 'checkbox', orderable: false },
            { data: 'id' },
            { data: 'cli.names' },
            { data: 'date_joined' },
            { data: 'subtotal' },
            { data: 'iva' },
            { data: 'total' },
            { data: 'actions', orderable: false }
        ],
        language: {
            url: languageUrl
        },
        columnDefs: [
            {
                targets: 0,
                render: function(data, type, row) {
                    return '<div class="form-check"><input class="form-check-input fs-15" type="checkbox" name="checkAll" value="option1"></div>';
                }
            },
        ]
    });

    $('#scroll-horizontal tbody').on('click', 'a[rel="details"]', function(e) {
        e.preventDefault();
        var tr = tblSale.cell($(this).closest('td, li')).index();
        var data = tblSale.row(tr.row).data();
        
        $('#tblDetail').DataTable({
            responsive: true,
            autowidth: false,
            destroy: true,
            deferRender: true,
            language: {
                url: languageUrl
            },
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data:{
                    'action': 'search_details_prod',
                    'id': data.id
                },
                dataSrc: ''
            },
            columns: [
                { data: 'prod.id' },
                { data: 'prod.name' },
                { data: 'prod.cate.name' },
                { data: 'price' },
                { data: 'cant' },
                { data: 'subtotal' },
            ],
            columnDefs: [
                {
                    targets: [-1, -3],
                    class: 'text-center',
                    orderable: false,
                    render: function(data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class : 'text-center',
                    orderable: false,
                    render: function(data, type, row) {
                        return data;
                    }
                }
            ],
            initComplete: function(settings, json) {
            },
        });

        $('#myModal').modal('show');
    });

});