$(document).ready(function () {
    const XAXISRANGE = 30000;
    
    var dataRealtime = []; 

    // Grafica de ventas por mes (Barras)
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
    // Fin de la grafica de ventas por mes

    // Grafica de ventas por productos (Pie)
    var optionsPie = {
        series: [],
        noData: {
            text: 'Cargando...'
        },
        chart: {
            width: 380,
            type: 'pie',
        },
        labels: [], // Añadir etiquetas para los nombres de los productos
        responsive: [{
            breakpoint: 480,
            options: {
                chart: {
                    width: 200
                },
                legend: {
                    position: 'bottom'
                }
            }
        }],
        tooltip: {
            y: {
                formatter: function (val) {
                    return parseFloat(val).toFixed(2) + "$"
                }
            }
        },
    };

    var pieChart = new ApexCharts(document.querySelector("#pieChart"), optionsPie);
    pieChart.render();
    // Fin de la grafica de ventas por productos

    // Grafica de ventas en tiempo real
    var onlineOptions = {
        series: [{
            data: dataRealtime.slice()
        }],
        noData: {
            text: 'Cargando...'
        },
        chart: {
            id: 'realtime',
            height: 350,
            type: 'line',
            animations: {
                enabled: true,
                easing: 'linear',
                dynamicAnimation: {
                    speed: 1000
                }
            },
            toolbar: {
                show: false
            },
            zoom: {
                enabled: false
            }
        },
        dataLabels: {
            enabled: false
        },
        stroke: {
            curve: 'smooth'
        },
        title: {
            text: 'Dynamic Updating Chart',
            align: 'left'
        },
        markers: {
            size: 0
        },
        xaxis: {
            type: 'datetime',
            range: XAXISRANGE,
        },
        yaxis: {
            max: 100
        },
        legend: {
            show: false
        },
    };

    var online = new ApexCharts(document.querySelector("#online"), onlineOptions);
    online.render();

    function updateRealtimeChart() {
        $.ajax({
            url: window.location.pathname,
            type: "POST",
            data: {
                'action': 'get_graph_online',
            },
            dataType: "json",
            success: function (response) {
                var newData = {
                    x: new Date().getTime(), // Current timestamp
                    y: response.y
                };
                dataRealtime.push(newData); // Agrega el nuevo punto de datos a la variable global
                online.updateSeries([{
                    data: dataRealtime
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

    var interval = window.setInterval(function () {
        updateRealtimeChart();
    }, 1000);
    // Fin de la grafica de ventas en tiempo real

    // Funcion para obtener los datos de la grafica de ventas por mes
    function get_graph_sales_year_month() {
        $.ajax({
            url: window.location.pathname,
            type: "POST",
            data: {
                'action': 'get_graph_sales_year_month',
            },
            dataType: "json",
            success: function (data) {
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

    // Funcion para obtener los datos de la grafica de ventas por productos
    function get_graph_sales_products_year_month() {
        $.ajax({
            url: window.location.pathname,
            type: "POST",
            data: {
                'action': 'get_graph_sales_products_year_month',
            },
            dataType: "json",
            success: function (data) {
                var seriesData = data.data.map(function (item) {
                    return item.y;
                });

                var labels = data.data.map(function (item) {
                    return item.name;
                });

                pieChart.updateOptions({
                    labels: labels
                });

                pieChart.updateSeries(seriesData);
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

    // Llamado a las funciones
    get_graph_sales_year_month();
    get_graph_sales_products_year_month();
});