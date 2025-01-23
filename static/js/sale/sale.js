$(document).ready(function () {
    var tblProducts;

    var vents = {
        items: {
            cli: '',
            date_joined: '',
            subtotal: 0.00,
            iva: 0.00,
            total: 0.00,
            products: []
        },
        calculate_invoce: function(){
            var subtotal = 0.00
            var iva = $('#id_iva').val()
            $.each(this.items.products, function(pos, dict){
                dict.subtotal = dict.quantity * parseFloat(dict.pvp)
                subtotal += dict.subtotal
            });
            this.items.subtotal = subtotal
            this.items.iva = (this.items.subtotal * iva) / 100
            this.items.total = this.items.subtotal + this.items.iva
    
            $('#id_subtotal').val(subtotal.toFixed(2))
            $('#ivacalc').val(this.items.iva.toFixed(2))
            $('#id_total').val(this.items.total.toFixed(2))
        },
        add: function(item){
            this.items.products.push(item)
            this.list()
        },
        list: function(){
            this.calculate_invoce()
            tblProducts = $('#invoice-table').DataTable({
                language: {
                    url: languageUrl
                },
                data: this.items.products,
                columns: [
                    { data: null, title: '#', render: (data, type, row, meta) => meta.row + 1 },
                    { data: 'name', title: 'Nombre del producto', render: (data) => `
                        <div class="mb-2">
                            <input type="text" class="form-control bg-light border-0" value="${data}" placeholder="Nombre del producto" required />
                            <div class="invalid-feedback">
                                Please enter a product name
                            </div>
                        </div>` 
                    },
                    { data: 'cate.name', title: 'Categoria', render: (data) => `
                        <div class="mb-2">
                            <input type="text" class="form-control bg-light border-0" value="${data}" placeholder="Categoria" required />
                            <div class="invalid-feedback">
                                Please enter a product name
                            </div>
                        </div>` 
                    },
                    { data: 'pvp', title: 'PVP', render: (data) => `
                        <div class="mb-2">
                            <input type="text" class="form-control bg-light border-0" value="${data}" placeholder="PVP" required />
                            <div class="invalid-feedback">
                                Please enter a product name
                            </div>
                        </div>` 
                    },
                    { data: 'pvp', title: 'Precio', render: (data) => `
                        <input type="number" class="form-control product-price bg-light border-0" value="${data}" step="0.01" placeholder="0.00" required />
                        <div class="invalid-feedback">
                            Please enter a rate
                        </div>` 
                    },
                    { data: 'quantity', title: 'Cantidad', render: (data) => `
                        <div class="input-step">
                            <input type="number" name="cant" class="product-quantity input-sm" value="${data}">
                        </div>` 
                    },
                    { data: 'subtotal', title: 'Subtotal', render: (data) => `
                        <input type="text" class="form-control bg-light border-0 product-line-price" value="${data}" placeholder="$0.00" readonly />` 
                    },
                    { data: null, title: 'Acciones', render: () => `
                        <a href="javascript:void(0)" class="btn btn-success remove-item" rel="remove">Eliminar</a>` 
                    }
                ],
                rowCallback: function(row, data, displayNum, displayIndex, dataIndex){
                    $(row).find('input[name="cant"]').TouchSpin({
                        min: 1,
                        max: 10000000000,
                        step: 1,
                    });
                },
                destroy: true // Destroy existing table before reinitializing
            });
        }
    }

    // TouchSpin of iva and calculate iva
    $("input[name='iva']").TouchSpin({
        min: 0,
        max: 101,
        step: 0.1,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%',
        buttondown_class: 'btn btn-secondary',
        buttonup_class: 'btn btn-secondary',
    }).on('change', function(){
        vents.calculate_invoce()
    });

    // Select 2
    $('#input-search').select2({
        theme: 'bootstrap-5', // Ensure the theme matches your Bootstrap version
        language: 'es',
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function(params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_products'
                };
                return queryParameters;
            },
            processResults: function(data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Buscar producto',
        minimumInputLength: 1,
    })
    // Event select2 (Add produts to the vents variable)
    .on('select2:select', function(e) {
        event.preventDefault
        var selectedItem = e.params.data;
        vents.add(selectedItem);
        // limpiar el input
        $('#input-search').val(null).trigger('change');
    });

    $('.btnRemoveAll').on('click', function(){
        if(vents.items.products.length === 0){
            return false
        }
        else{
            showModal(
                'bx bxs-calendar-exclamation', // iconClass
                'Confirmación', // title
                '¿Estás seguro de que deseas eliminar todos los productos?', // message
                'Cancelar', // button1Text
                'close', // button1Action
                'Confirmar', // button2Text
                function() { // button2Action
                    vents.items.products = [];
                    vents.list();
                    $('#dynamic_modal').modal('hide');
                }
            );
        }
    });

    $('#invoice-table tbody')
    .on('click', 'a[rel="remove"]', function(){
        var tr = tblProducts.cell($(this).closest('td, li')).index();
        showModal(
            'bx bxs-calendar-exclamation', // iconClass
            'Confirmación', // title
            '¿Estás seguro de que deseas eliminar este los productos?', // message
            'Cancelar', // button1Text
            'close', // button1Action
            'Confirmar', // button2Text
            function() { // button2Action
                vents.items.products.splice(tr.row,1);
                vents.list();
                $('#dynamic_modal').modal('hide');
            }
        );
    })
    .on('change', 'input[name="cant"]', function(){
        // we get the quantity
        var cant = parseInt($(this).val());
        // We get thw position update cell position
        var tr = tblProducts.cell($(this).closest('td, li')).index();
        // Update the quantity
        vents.items.products[tr.row].quantity = cant;
        // Calculate the invoce
        vents.calculate_invoce();
        // Update subtotal with function .node() of datatables
        $('td:eq(6)', tblProducts.row(tr.row).node()).html(`<input type="text" class="form-control bg-light border-0 product-line-price" value="${vents.items.products[tr.row].subtotal.toFixed(2)} $" placeholder="$0.00" readonly />`);
    });

    // event submit
    $('#form-sales').on('submit', function(e){
        e.preventDefault();
        if(vents.items.products.length === 0){
            showModal(
                'bx bxs-message-alt-x', // iconClass
                'ERROR!', // title
                'Por favor seleccione al menos 1 item en su detalle de venta', // message
                'Cancelar', // button1Text
                'close', // button1Action
                'Cerrar', // button2Text
                'colorIcon', '#f06548',
                function() {
                    $('#dynamic_modal').modal('hide');
                }
            );
        }else{
            vents.items.date_joined = $('input[name="date_joined"]').val();
            vents.items.cli = $('#id_cli').val();
        
            var formData = new FormData(this);
            var parameters = {};
            formData.forEach((value, key) => {
                parameters[key] = value;
            });
            parameters['action'] = $('#action_data').val(); // Asegúrate de que 'action' se está incluyendo
            parameters['vents'] = JSON.stringify(vents.items);
            submit_with_ajax(
                window.location.pathname,
                'Notificación',
                '¿Estas seguro de realizar la siguiente acción?',
                parameters,
                function(){
                    location.href = '/erp/sale/list/';
                }
            );
                
        }
    });

    console.log(det)
    vents.items.products = det
    vents.list();
});
