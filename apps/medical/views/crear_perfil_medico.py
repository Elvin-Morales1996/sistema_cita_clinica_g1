from django.shortcuts import render, redirect
from apps.forms_medico import PerfilMedicoForm
from django.core.mail import send_mail
from django.conf import settings

def crear_perfil_medico(request):
    if request.method == 'POST':
        form = PerfilMedicoForm(request.POST)
        if form.is_valid():
            medico = form.save()  # Guardamos y obtenemos la instancia creada
            
            # Enviar correo
            subject = 'Registro de Médico Exitoso'
            message = f'Hola {medico.nombre},\n\nTu perfil de médico ha sido creado exitosamente.'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [medico.email]  # Asumiendo que el modelo tiene campo email
            
            send_mail(subject, message, from_email, recipient_list)
            
            return redirect('home')
    else:
        form = PerfilMedicoForm()
    return render(request, 'medical/crear_perfil_medico.html', {'form': form})