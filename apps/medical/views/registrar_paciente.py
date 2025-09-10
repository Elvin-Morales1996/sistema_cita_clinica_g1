from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from apps.forms_paciente import PacienteForm

def registrar_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save()  
            messages.success(request, '¡El registro se realizó con éxito!')
            try:
                send_mail(
                    subject='Registro Exitoso',
                    message=f'Hola {paciente.nombre}, Se.',
                    from_email=None,  
                    recipient_list=[paciente.contacto], 
                    fail_silently=False,
                )
            except Exception as e:
                messages.warning(request, f'No se pudo enviar el correo: {e}')

            # Redirigir para limpiar el formulario
            return redirect('registrar_paciente')
    else:
        form = PacienteForm()

    return render(request, 'medical/registrar_paciente.html', {'form': form})
