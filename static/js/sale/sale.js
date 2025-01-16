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
        add: function(){
            
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

    // Initialize DataTable
    $('.invoice-table').DataTable({
        paging: false,
        searching: false,
        info: false,
        ordering: false
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

    // Add new item row
    function addItemRow() {
        var tableBody = $('#newlink');
        var rowCount = tableBody.find('tr').length;
        var newRow = $(`
            <tr class="product">
                <th scope="row" class="product-id">${rowCount + 1}</th>
                <td class="text-start">
                    <div class="mb-2">
                        <input type="text" class="form-control bg-light border-0" placeholder="Nombre del producto" required />
                        <div class="invalid-feedback">
                            Please enter a product name
                        </div>
                    </div>
                </td>
                <td class="text-start">
                    <div class="mb-2">
                        <input type="text" class="form-control bg-light border-0" placeholder="Categoria" required />
                        <div class="invalid-feedback">
                            Please enter a product name
                        </div>
                    </div>
                </td>
                <td class="text-start">
                    <div class="mb-2">
                        <input type="text" class="form-control bg-light border-0" placeholder="PVP" required />
                        <div class="invalid-feedback">
                            Please enter a product name
                        </div>
                    </div>
                </td>
                <td>
                    <input type="number" class="form-control product-price bg-light border-0" step="0.01" placeholder="0.00" required />
                    <div class="invalid-feedback">
                        Please enter a rate
                    </div>
                </td>
                <td>
                    <div class="input-step">
                        <button type="button" class='minus'>–</button>
                        <input type="number" class="product-quantity" value="0" readonly>
                        <button type="button" class='plus'>+</button>
                    </div>
                </td>
                <td class="text-end">
                    <div>
                        <input type="text" class="form-control bg-light border-0 product-line-price" placeholder="$0.00" readonly />
                    </div>
                </td>
                <td class="product-removal">
                    <a href="javascript:void(0)" class="btn btn-success remove-item">Eliminar</a>
                </td>
            </tr>
        `);
        tableBody.append(newRow);
        initializeQuantityButtons();
        initializeRemoveButtons();
    }

    // Initialize remove buttons
    function initializeRemoveButtons() {
        $('.remove-item').off('click').on('click', function () {
            $(this).closest('tr').remove();
            updateTotal();
        });
    }

    // Initialize the form
    function initializeForm() {
        initializeQuantityButtons();
        initializeRemoveButtons();
        updateTotal();
        $('#add-item').on('click', addItemRow);
    }

    initializeForm();
});