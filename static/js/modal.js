function showModal(
    iconClass, title, message, button1Text, button1Action, button2Text, button2Action, 
    colorIcon="#25a0e2", id="dynamic_modal", id_button_1="button1", id_button_2="button2"
    ){
    var modalHtml = `
        <div class="modal fade bs-example-modal-center" id="${id}" tabindex="-1" role="dialog" aria-labelledby="confirmationModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-body text-center p-5">
                        <i class="${iconClass}" style="font-size: 120px; color: ${colorIcon};"></i>
                        <div class="mt-4">
                            <h4 class="mb-3">${title}</h4>
                            <p class="text-muted mb-4">${message}</p>
                            <div class="hstack gap-2 justify-content-center">
                                <button type="button" class="btn btn-light" id="${id_button_1}">${button1Text}</button>
                                <button type="button" class="btn btn-primary" id="${id_button_2}">${button2Text}</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    $('body').append(modalHtml);
    $('#'+ id).modal('show');

    $('#'+ id_button_1 ).on('click', function() {
        if (button1Action === 'close') {
            $('#'+ id).modal('hide');
        } else if (typeof button1Action === 'function') {
            button1Action();
        }
    });

    $('#'+ id_button_2).on('click', function() {
        if (typeof button2Action === 'function') {
            button2Action();
        }
    });

    $('#'+ id).on('hidden.bs.modal', function () {
        $(this).remove();
    });
}
