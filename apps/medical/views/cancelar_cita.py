from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from apps.medical.models.cita import Cita
from apps.medical.utils.email_utils import send_cita_notification_email
from smtplib import SMTPException

def cancelar_cita(request, cita_id):
    # Obtener la cita o devolver 404 si no existe
    cita = get_object_or_404(Cita, id=cita_id)

    if request.method == 'POST':
        # Cambiar estado y guardar
        cita.estado = 'cancelada'
        cita.save()
        messages.success(request, '¡La cita ha sido cancelada con éxito!')

        # Intentar enviar notificación por correo de manera segura
        try:
            enviado = send_cita_notification_email(cita, 'Cita Cancelada', 'canceled')
            if enviado:
                messages.info(request, 'Se ha enviado una notificación por correo electrónico.')
            else:
                messages.warning(request, 'La cita se canceló, pero no se pudo enviar el correo de notificación.')
        except SMTPException as e:
            # Captura errores SMTP para que no rompa la aplicación
            messages.warning(request, f'La cita se canceló, pero ocurrió un error al enviar el correo: {e}')

        # Redirigir al home
        return redirect('home')

    # Mostrar la plantilla de confirmación de cancelación
    return render(request, 'medical/cancelar_cita.html', {'cita': cita})
