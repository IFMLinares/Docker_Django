function showModal(iconClass, title, message, button1Text, button1Action, button2Text, button2Action) {
    var modalHtml = `
        <div class="modal fade bs-example-modal-center" id="dynamic_modal" tabindex="-1" role="dialog" aria-labelledby="confirmationModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-body text-center p-5">
                        <i class="${iconClass}" style="font-size: 120px; color: #25a0e2;"></i>
                        <div class="mt-4">
                            <h4 class="mb-3">${title}</h4>
                            <p class="text-muted mb-4">${message}</p>
                            <div class="hstack gap-2 justify-content-center">
                                <button type="button" class="btn btn-light" id="button1">${button1Text}</button>
                                <button type="button" class="btn btn-primary" id="button2">${button2Text}</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    $('body').append(modalHtml);
    $('#dynamic_modal').modal('show');

    $('#button1').on('click', function() {
        if (button1Action === 'close') {
            $('#dynamic_modal').modal('hide');
        } else if (typeof button1Action === 'function') {
            button1Action();
        }
    });

    $('#button2').on('click', function() {
        if (typeof button2Action === 'function') {
            button2Action();
        }
    });

    $('#dynamic_modal').on('hidden.bs.modal', function () {
        $(this).remove();
    });
}
