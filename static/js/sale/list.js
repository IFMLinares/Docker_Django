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
            {
                targets: 7,
                render: function(data, type, row) {
                    return `
                        <a href="${row.get_update_url}" class="btn btn-primary waves-effect waves-light">
                            <i class="bx bx-edit-alt"></i>
                        </a>
                        <a href="${row.get_delete_url}" class="btn btn-danger waves-effect waves-light">
                            <i class="bx bx-trash-alt"></i>
                        </a>
                        <a href="#" rel="details" class="btn btn-success waves-effect waves-light">
                            <i class="bx bx-search-alt"></i>
                        </a>
                    `;
                }
            }
        ]
    });

    $('#scroll-horizontal tbody').on('click', 'a[rel="details"]', function(e) {
        e.preventDefault();
        var tr = tblSale.cell($(this).closest('td, li')).index();
        var data = tblSale.row(tr.row).data();
        
    });
});