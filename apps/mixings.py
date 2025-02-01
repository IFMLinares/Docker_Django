from django.contrib import messages
from django.db import transaction

class FormMessagesMixin:
    type_operation = 'create'
    def handle_form_messages(self, form, operation):
        if form.is_valid():
            if operation == 'create':
                messages.success(self.request, 'El registro se ha guardado correctamente.')
            elif operation == 'update':
                messages.success(self.request, 'El registro se ha actualizado correctamente.')
            elif operation == 'delete':
                messages.success(self.request, 'El registro se ha eliminado correctamente.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(self.request, f"{field}: {error}")
    
    @transaction.atomic
    def form_valid(self, form):
        response = super().form_valid(form)
        self.handle_form_messages(form, self.type_operation)
        return response
    
    @transaction.atomic
    def form_invalid(self, form):
        self.handle_form_messages(form, self.type_operation)
        return super().form_invalid(form)