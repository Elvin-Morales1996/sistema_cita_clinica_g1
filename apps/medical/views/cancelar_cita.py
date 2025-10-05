from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from apps.medical.models.cita import Cita
from apps.medical.utils.email_utils import send_cita_notification_email

def cancelar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)

    if request.method == 'POST':
        cita.estado = 'cancelada'
        cita.save()
        messages.success(request, '¡La cita ha sido cancelada con éxito!')

        # Enviar notificación por correo
        if send_cita_notification_email(cita, 'Cita Cancelada', 'canceled'):
            messages.info(request, 'Se ha enviado una notificación por correo electrónico.')
        else:
            messages.warning(request, 'La cita se canceló, pero no se pudo enviar el correo de notificación.')

        return redirect('home')

    return render(request, 'medical/cancelar_cita.html', {'cita': cita})