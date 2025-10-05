from django.shortcuts import render, redirect
from apps.forms_medico import PerfilMedicoForm
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

def crear_perfil_medico(request):
    if request.method == 'POST':
        form = PerfilMedicoForm(request.POST)
        if form.is_valid():
            medico = form.save()  # Guardamos y obtenemos la instancia creada
            
            messages.success(request, '¡El perfil del médico se creó con éxito!')

            # Intentar enviar correo sin romper la vista
            try:
                subject = 'Registro de Médico Exitoso'
                message = f'Hola {medico.nombre},\n\nTu perfil de médico ha sido creado exitosamente.'
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [medico.email]  # Asumiendo que el modelo tiene campo email

                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            except Exception as e:
                messages.warning(request, f'No se pudo enviar el correo: {e}')
            
            return redirect('home')
    else:
        form = PerfilMedicoForm()
    
    return render(request, 'medical/crear_perfil_medico.html', {'form': form})
