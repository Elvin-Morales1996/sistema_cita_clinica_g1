from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from apps.medical.models.cita import Cita
from apps.forms_cita import CitaForm
from apps.medical.utils.email_utils import send_cita_notification_email

def editar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)

    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            messages.success(request, '¡La cita se modificó con éxito!')

            # Enviar notificación por correo
            if send_cita_notification_email(cita, 'Cita Modificada', 'modified'):
                messages.info(request, 'Se ha enviado una notificación por correo electrónico.')
            else:
                messages.warning(request, 'La cita se modificó, pero no se pudo enviar el correo de notificación.')

            return redirect('home')
    else:
        form = CitaForm(instance=cita)

    return render(request, 'medical/editar_cita.html', {'form': form, 'cita': cita})