# views/crear_cita.py
from django.shortcuts import render, redirect
from django.contrib import messages
from apps.forms_cita import CitaForm
from apps.medical.utils.email_utils import send_cita_notification_email

def crear_cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save()  # Guardamos la cita

            # Mensaje de éxito en pantalla
            messages.success(request, '¡La cita se registró con éxito!')

            # Enviar notificación por correo
            if send_cita_notification_email(cita, 'Cita Registrada', 'created'):
                messages.info(request, 'Se ha enviado una confirmación por correo electrónico.')
            else:
                messages.warning(request, 'La cita se registró, pero no se pudo enviar el correo de confirmación.')

            return redirect('crear_cita')  # Redirige a la misma página para limpiar el formulario
    else:
        form = CitaForm()

    return render(request, 'medical/Formulariocitas.html', {'form': form})
