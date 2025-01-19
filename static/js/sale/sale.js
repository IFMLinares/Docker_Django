$(document).ready(function () {

    var vents = {
        items: {
            cli: '',
            date_joined: '',
            subtotal: 0.00,
            iva: 0.00,
            total: 0.00,
            products: []
        },
        add: function(item){
            this.items.products.push(item)
            this.list()
        },
        list: function(){
            var tableBody = $('#newlink');
            tableBody.empty(); // Clear existing rows

            this.items.products.forEach((product, index) => {
                var newRow = $(`
                    <tr class="product">
                        <th scope="row" class="product-id">${index + 1}</th>
                        <td class="text-start">
                            <div class="mb-2">
                                <input type="text" class="form-control bg-light border-0" value="${product.name}" placeholder="Nombre del producto" required />
                                <div class="invalid-feedback">
                                    Please enter a product name
                                </div>
                            </div>
                        </td>
                        <td class="text-start">
                            <div class="mb-2">
                                <input type="text" class="form-control bg-light border-0" value="${product.cate.name}" placeholder="Categoria" required />
                                <div class="invalid-feedback">
                                    Please enter a product name
                                </div>
                            </div>
                        </td>
                        <td class="text-start">
                            <div class="mb-2">
                                <input type="text" class="form-control bg-light border-0" value="${product.pvp}" placeholder="PVP" required />
                                <div class="invalid-feedback">
                                    Please enter a product name
                                </div>
                            </div>
                        </td>
                        <td>
                            <input type="number" class="form-control product-price bg-light border-0" value="${product.pvp}" step="0.01" placeholder="0.00" required />
                            <div class="invalid-feedback">
                                Please enter a rate
                            </div>
                        </td>
                        <td>
                            <div class="input-step">
                                <button type="button" class='minus'>–</button>
                                <input type="number" class="product-quantity" value="${product.quantity}" readonly>
                                <button type="button" class='plus'>+</button>
                            </div>
                        </td>
                        <td class="text-end">
                            <div>
                                <input type="text" class="form-control bg-light border-0 product-line-price" value="${(product.pvp * product.quantity).toFixed(2)}" placeholder="$0.00" readonly />
                            </div>
                        </td>
                        <td class="product-removal">
                            <a href="javascript:void(0)" class="btn btn-success remove-item">Eliminar</a>
                        </td>
                    </tr>
                `);
                tableBody.append(newRow);
            });

            initializeQuantityButtons();
            initializeRemoveButtons();
        }
    }

    $("input[name='iva']").TouchSpin({
        min: 0,
        max: 100,
        step: 0.1,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%',
        buttondown_class: 'btn btn-secondary',
        buttonup_class: 'btn btn-secondary',
    });


    // Initialize quantity buttons
    function initializeQuantityButtons() {
        $('.input-step .plus').off('click').on('click', function () {
            var input = $(this).prev('input');
            input.val(parseInt(input.val()) + 1);
            updateTotal();
        });

        $('.input-step .minus').off('click').on('click', function () {
            var input = $(this).next('input');
            input.val(Math.max(0, parseInt(input.val()) - 1));
            updateTotal();
        });
    }

    // Update total
    function updateTotal() {
        var subtotal = parseFloat($('input[name="subtotal"]').val()) || 0;
        var iva = parseFloat($('input[name="iva"]').val()) || 0;
        var total = subtotal + iva;
        $('input[name="total"]').val(total.toFixed(2));
    }

    // Initialize remove buttons
    function initializeRemoveButtons() {
        $('.remove-item').off('click').on('click', function () {
            $(this).closest('tr').remove();
            updateTotal();
        });
    }

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

    // jquery ui
    // $('#input-search').autocomplete({
    //     source: function(request, response) {
    //         $.ajax({
    //             url: window.location.pathname,
    //             type: 'POST',
    //             data: {
    //                 term: request.term,
    //                 action: 'search_products'
    //             },
    //             dataType: 'json',
    //             success: function(data) {
    //                 response(data);
    //             },
    //             fail: function() {
    //                 alert('There was an error');
    //             }
    //         });
    //     },
    //     delat: 500,
    //     minLength: 1,
    //     select: function(event, ui) {
    //         console.log(ui.item);
    //     }
    // });

});