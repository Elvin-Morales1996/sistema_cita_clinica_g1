from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from apps.medical.models.usuario import Usuario
from apps.audit.models import AuditLog
from django.utils import timezone
from django.contrib import messages

def login_view(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        next_url = request.GET.get("next") or "home"

        # Validación de campos vacíos
        if not username or not password:
            error_message = "Usuario y contraseña son requeridos"
        else:
            try:
                usuario = Usuario.objects.get(usuario__iexact=username)
                
                if check_password(password, usuario.clave):
                    
                    if getattr(usuario, "estado", "A") != "A":
                        error_message = "Tu usuario está inactivo. Contacta al administrador."
                        messages.error(request, error_message)
                        return render(request, "medical/login.html", {
                                "error": error_message,
                                "username": username,
                            })
                    
                    # LOGIN EXITOSO
                    request.session['user_id'] = usuario.id
                    request.session['username'] = usuario.usuario
                    request.session['rol'] = usuario.rol
                    request.session['estado'] = usuario.estado 
                    request.session["is_superadmin"] = (usuario.usuario.strip().lower() == "erick"
                                                        and usuario.rol == "Administrador")
                    
                    # Registrar en AuditLog SOLO si login es exitoso
                    AuditLog.objects.create(
                        usuario=usuario,  
                        accion='login',
                        detalles=f"Inicio de sesión exitoso para el usuario '{usuario.usuario}'"
                    )
                    return redirect(next_url)
                else:
                    error_message = "Usuario o contraseña incorrectos"
            except Usuario.DoesNotExist:
                error_message = "Usuario o contraseña incorrectos"

    return render(request, 'medical/login.html', {'error': error_message})


def logout_view(request):
    # Registrar logout si hay usuario en sesión
    if 'user_id' in request.session:
        try:
            usuario = Usuario.objects.get(id=request.session['user_id'])
            AuditLog.objects.create(
                usuario=usuario,  
                accion='logout', 
                detalles=f"Cierre de sesión para el usuario '{usuario.usuario}'"
            )
        except Usuario.DoesNotExist:
            pass
    
    request.session.flush()  
    return redirect('login')
