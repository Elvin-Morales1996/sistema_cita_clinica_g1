# views/registrar_paciente.py
from django.shortcuts import render, redirect
from django.contrib import messages
from apps.forms_paciente import PacienteForm
from apps.medical.utils.email_utils import send_cita_notification_email  # reutilizamos la función

def registrar_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save()  # Guardamos al paciente
            messages.success(request, '¡El registro se realizó con éxito!')

            # Enviar notificación por correo usando la misma función que en crear_cita
            if send_cita_notification_email(paciente, 'Registro Exitoso', 'created'):
                messages.info(request, 'Se ha enviado una confirmación por correo electrónico.')
            else:
                messages.warning(request, 'El registro se realizó, pero no se pudo enviar el correo de confirmación.')

            return redirect('registrar_paciente')  # Redirige a la misma página para limpiar el formulario
    else:
        form = PacienteForm()

    return render(request, 'medical/registrar_paciente.html', {'form': form})
