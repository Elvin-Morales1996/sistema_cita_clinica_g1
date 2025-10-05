# views/registrar_paciente.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from apps.forms_paciente import PacienteForm

def registrar_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save()  # Guardamos al paciente
            messages.success(request, '¡El registro se realizó con éxito!')

            # Intentar enviar correo sin que rompa la vista
            try:
                send_mail(
                    subject='Registro Exitoso',
                    message=f'Hola {paciente.nombre} {paciente.apellido}, tu registro fue exitoso.',
                    from_email=settings.DEFAULT_FROM_EMAIL,  # Remitente válido
                    recipient_list=[paciente.contacto],       # Email del paciente
                    fail_silently=False,                       # Lanzará excepción si falla
                )
            except Exception as e:
                # Solo mostrar advertencia, no romper la app
                messages.warning(request, f'No se pudo enviar el correo: {e}')

            # Redirigir para limpiar el formulario
            return redirect('registrar_paciente')
    else:
        form = PacienteForm()

    return render(request, 'medical/registrar_paciente.html', {'form': form})
