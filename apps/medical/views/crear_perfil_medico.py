# views/crear_perfil_medico.py
from django.shortcuts import render, redirect
from django.contrib import messages
from apps.forms_medico import PerfilMedicoForm
from apps.medical.utils.email_utils import send_cita_notification_email  # reutilizamos la función

def crear_perfil_medico(request):
    if request.method == 'POST':
        form = PerfilMedicoForm(request.POST)
        if form.is_valid():
            medico = form.save()  # Guardamos la instancia
            messages.success(request, '¡El perfil del médico se creó con éxito!')

            # Enviar notificación por correo
            if send_cita_notification_email(medico, 'Registro de Médico Exitoso', 'created'):
                messages.info(request, 'Se ha enviado una confirmación por correo electrónico.')
            else:
                messages.warning(request, 'El perfil se creó, pero no se pudo enviar el correo de confirmación.')

            return redirect('home')
    else:
        form = PerfilMedicoForm()

    return render(request, 'medical/crear_perfil_medico.html', {'form': form})
