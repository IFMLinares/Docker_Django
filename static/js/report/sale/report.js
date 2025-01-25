var date_range = null;
var date_now = new moment().format('DD-MM-YYYY');

function generate_report(){
    var parameters = {
        'action': 'search_report',
        'start_date': new moment().format('YYYY-MM-DD'),
        'end_date': new moment().format('YYYY-MM-DD'),
    };

    if(date_range != null){
        parameters['start_date'] = date_range.startDate.format('YYYY-MM-DD');
        parameters['end_date'] = date_range.endDate.format('YYYY-MM-DD');
    }

    $('#scroll-horizontal').dataTable({
        resposive: true,
        autowidth: false,
        destroy: true,
        deferRender: true,
        order: false,
        pagin: false,
        ordering: false,
        searching: false,
        info: false,
        paging: false,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: parameters,
            dataSrc: ''
        },
        columnDefs: [
            {
                targets: [-1, -2, -3],
                class: 'text-center',
                oderable: false,
                render: function(data, type, row){
                    return '$' + parseFloat(data).toFixed(2);
                }
            }
        ],
        initComplete: function(settings, json){
        },
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'excel',
                text: 'Descargar Excel <i class="las la-file-excel" style="font-size: 18px;"></i>',
                titleAttr: 'Excel',
                className: 'btn btn-success btn-flat btn-xs'
            },
            {
                extend: 'pdf',
                text: 'Descargar Pdf <i class="las la-file-pdf" style="font-size: 18px;"></i>',
                titleAttr: 'PDF',
                className: 'btn btn-danger btn-flat btn-xs',
                download: 'open',
                orientation: 'landscape',
                pageSize: 'LEGAL',
                customize: function (doc) {
                    doc.styles = {
                        header: {
                            fontSize: 18,
                            bold: true,
                            alignment: 'center'
                        },
                        subheader: {
                            fontSize: 13,
                            bold: true
                        },
                        quote: {
                            italics: true
                        },
                        small: {
                            fontSize: 8
                        },
                        tableHeader: {
                            bold: true,
                            fontSize: 11,
                            color: 'white',
                            fillColor: '#2d4154',
                            alignment: 'center'
                        }
                    };
                    doc.content[1].table.widths = ['20%','20%','15%','15%','15%','15%'];
                    doc.content[1].margin = [0, 35, 0, 0];
                    doc.content[1].layout = {};
                    doc['footer'] = (function (page, pages) {
                        return {
                            columns: [
                                {
                                    alignment: 'left',
                                    text: ['Fecha de creación: ', {text: date_now}]
                                },
                                {
                                    alignment: 'right',
                                    text: ['página ', {text: page.toString()}, ' de ', {text: pages.toString()}]
                                }
                            ],
                            margin: 20
                        }
                    });

                }
            }
        ],

    })
}

$(function(){
    $('#id_date_range').daterangepicker({
        locale:{
            format: 'DD/MM/YYYY',
            applyLabel: '<i class=" bx bx-calendar-check"></i> Aplicar',
            cancelLabel: '<i class="bx bx-calendar-x"></i> Cancelar',
        }
    }).on('apply.daterangepicker', function(ev, picker){
        date_range = picker;
        generate_report();
    }).on('cancel.daterangepicker', function(ev, picker){
        console.log(date_now)
        $(this).data('daterangepicker').setStartDate(date_now);
        $(this).data('daterangepicker').setEndDate(date_now);
        date_range = picker;
        generate_report();
    });
    generate_report();
});