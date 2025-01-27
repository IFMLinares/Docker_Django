var options = {
    series: [],
    chart: {
        type: 'bar',
        height: 380
    },
    noData: {
        text: 'Cargando...'
    },
    plotOptions: {
        bar: {
            horizontal: false,
            columnWidth: '55%',
            distributed: true // Esta propiedad distribuye los colores
        },
    },
    dataLabels: {
        enabled: false
    },
    stroke: {
        show: true,
        width: 2,
        colors: ['transparent']
    },
    xaxis: {
        categories: month_list,
    },
    yaxis: {
        title: {
            text: 'Valores $'
        }
    },
    fill: {
        opacity: 1
    },
    tooltip: {
        y: {
            formatter: function (val) {
                return parseFloat(val).toFixed(2) + "$"
            }
        }
    },
};

var chart = new ApexCharts(document.querySelector("#chart"), options);
chart.render();

function get_graph_sales_year_month() {
    $.ajax({
        url: window.location.pathname,
        type: "POST",
        data: {
            'action': 'get_graph_sales_year_month',
        },
        dataType: "json",
        success: function (data) {
            console.log(data);
            chart.updateSeries([{
                name: 'Ventas: ',
                data: data
            }]);
        },
        error: function (xhr, errmsg, err) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Ocurrió un error al cargar los datos',
            });
        }
    });
}

$(document).ready(function () {
    get_graph_sales_year_month();
});