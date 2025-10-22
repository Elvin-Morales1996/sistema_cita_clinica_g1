from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from apps.medical.models.usuario import Usuario


def login_view(request):
    error_message = None

    if request.method == 'POST':
        username = (request.POST.get('username') or '').strip()
        password = (request.POST.get('password') or '')

        try:
            usuario = Usuario.objects.get(usuario__iexact=username)
        except Usuario.DoesNotExist:
            error_message = "Usuario o contraseña incorrectos"
        else:
            if check_password(password, usuario.clave):
                # Bloquear acceso si el usuario está INACTIVO (estado != 'A')
                if getattr(usuario, 'estado', 'A') != 'A':
                    error_message = "Tu usuario está inactivo. Contacta al administrador."
                    # Si usas mensajes en la plantilla:
                    messages.error(request, error_message)
                    return render(request, 'medical/login.html', {
                        'error': error_message,
                        'username': username,
                    })

                # Guardar sesión
                request.session['user_id'] = usuario.id
                request.session['username'] = usuario.usuario
                request.session['rol'] = usuario.rol

                # Flag para superadministrador (solo 'Erick', case-insensitive)
                request.session['is_superadmin'] = (
                    usuario.usuario.strip().lower() == 'erick'
                    and usuario.rol == 'Administrador'
                )

                return redirect('home')
            else:
                error_message = "Usuario o contraseña incorrectos"

    return render(request, 'medical/login.html', {'error': error_message})


def logout_view(request):
    request.session.flush()  # ✅ cierra la sesión
    return redirect('login')
