from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from apps.medical.models.usuario import Usuario
from apps.audit.models import AuditLog
from django.utils import timezone


def login_view(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password')

        try:
            usuario = Usuario.objects.get(usuario__iexact=username)
        except Usuario.DoesNotExist:
            error_message = "Usuario o contraseña incorrectos"
        else:
            if check_password(password, usuario.clave):
                request.session['user_id'] = usuario.id
                request.session['username'] = usuario.usuario
                request.session['rol'] = usuario.rol
                
            AuditLog.objects.create(
        usuario=None,  
        accion='login',
        detalles=f"Inicio de sesión exitoso para el usuario '{usuario.usuario}' a las {timezone.now()}."
    )
            return redirect('home')
    else:
            error_message = "Usuario o contraseña incorrectos"

    return render(request, 'medical/login.html', {'error': error_message})


def logout_view(request):
    request.session.flush()  
    return redirect('login')
